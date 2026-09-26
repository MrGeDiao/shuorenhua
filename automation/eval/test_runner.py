"""离线 fixture 验证 runner；这些测试不会启动模型 CLI。"""
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import runner


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        (self.repo / "SKILL.md").write_text("规则原文")
        self.run = self.root / "run"
        self.plan = dict(phase="rewrite", protocol="shuorenhua-rewrite-v1", provider="claude",
                         model="claude-opus-5", instructions="保留原意", candidate_files=["SKILL.md"],
                         max_calls=3, batch_size=1, timeout_seconds=20,
                         cases=[dict(id="B-01", source="原文。", request="轻改")])

    def prepare(self, **changes):
        self.plan.update(changes)
        runner.prepare(self.plan, self.repo, self.run)

    def bundle(self, *, provider="claude", answer=None, changes=None):
        plan, manifest = runner.load_run(self.run)
        prompt = (self.run / "batches/0001/prompt.txt").read_text()
        answer = answer or json.dumps({"cases": [{"id": "B-01", "text": "原文。"}]}, ensure_ascii=False)
        session = "fixture-session"
        if provider == "claude":
            raw = dict(subtype="success", is_error=False, stop_reason="end_turn", permission_denials=[],
                       result=answer, session_id=session, modelUsage={plan["model"]: {"provider": "firstParty"}})
            events = [dict(type="user", sessionId=session, message=dict(role="user", content=prompt)),
                      dict(type="assistant", sessionId=session, message=dict(role="assistant", model=plan["model"], content=[dict(type="text", text=answer)]))]
            signals = None
        else:
            raw = dict(stopReason="end_turn", text=answer, sessionId=session)
            events = [dict(type="user", prompt_index=0, content=prompt),
                      dict(type="assistant", model_id=plan["model"] + "-build", model_fingerprint="fixture-build", content=answer)]
            signals = dict(primaryModelId="grok-other", modelsUsed=["grok-other", plan["model"]])
        if changes:
            changes(raw, events)
        directory = self.root / ("bundle-" + str(len(list(self.root.glob("bundle-*")))))
        directory.mkdir()
        write_json(directory / "output.json", raw)
        transcript = directory / (session + ".jsonl")
        if provider == "grok":
            (directory / session).mkdir()
            transcript = directory / session / "chat_history.jsonl"
        transcript.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in events) + "\n")
        write_json(directory / "completion.json", {"exit_code": 0, "timed_out": False})
        if signals:
            write_json(transcript.parent / "signals.json", signals)
        return directory

    def ingest(self, bundle, **kwargs):
        transcript = next(bundle.rglob("*.jsonl"))
        return runner.import_result(self.run, 1, bundle / "output.json", transcript,
                                    bundle / "completion.json", signals=(transcript.parent / "signals.json") if (transcript.parent / "signals.json").exists() else None,
                                    **kwargs)

    def test_prepare_freezes_prompt_and_is_non_overwriting(self):
        self.prepare()
        plan, manifest = runner.load_run(self.run)
        self.assertEqual(len(manifest["batches"]), 1)
        self.assertIn("原文。", (self.run / "batches/0001/prompt.txt").read_text())
        with self.assertRaises(runner.RunnerError):
            runner.prepare(self.plan, self.repo, self.run)

    def test_json_artifact_requires_object(self):
        path = self.root / "artifact.json"
        for value in ([], [1], "text", 1, True, None):
            with self.subTest(value=value):
                write_json(path, value)
                with self.assertRaises(runner.RunnerError):
                    runner.read_json(path)

    def test_non_object_completion_records_failed_validation(self):
        self.prepare()
        bundle = self.bundle()
        write_json(bundle / "completion.json", [])
        report = self.ingest(bundle)
        self.assertFalse(report["valid"])
        attempt = self.run / "batches/0001/attempts/0001"
        self.assertFalse(runner.read_json(attempt / "validation.json")["valid"])

    def test_plan_rejects_duplicate_ids_bad_batch_and_missing_judge_outputs(self):
        for delta in [dict(cases=self.plan["cases"] * 2), dict(batch_size=16), dict(max_calls=0),
                      dict(phase="judge", protocol="shuorenhua-judge-v1", rubric="规则", outputs={})]:
            plan = dict(self.plan, **delta)
            with self.subTest(delta=delta), self.assertRaises(runner.RunnerError):
                runner.prepare(plan, self.repo, self.run)

    def test_candidate_change_invalidates_run(self):
        self.prepare()
        (self.repo / "SKILL.md").write_text("规则变化")
        with self.assertRaises(runner.RunnerError):
            runner.load_run(self.run)

    def test_prompt_tampering_invalidates_run(self):
        self.prepare()
        (self.run / "batches/0001/prompt.txt").write_text("不同指令")
        with self.assertRaises(runner.RunnerError):
            runner.load_run(self.run)

    def test_harness_change_does_not_invalidate_verified_generation(self):
        self.prepare()
        self.ingest(self.bundle())
        with mock.patch.object(runner, "harness_hash", return_value="new-validator-code"):
            self.assertTrue(runner.resume(self.run)["complete"])

    def test_model_or_instructions_change_invalidates_run(self):
        self.prepare()
        plan = runner.read_json(self.run / "plan.json")
        plan["instructions"] = "另一份规则"
        write_json(self.run / "plan.json", plan)
        with self.assertRaises(runner.RunnerError):
            runner.load_run(self.run)

    def test_offline_claude_success_reuses_without_subprocess(self):
        self.prepare()
        self.assertTrue(self.ingest(self.bundle())["valid"])
        with mock.patch.object(runner.subprocess, "run", side_effect=AssertionError("禁止真实调用")):
            self.assertTrue(runner.resume(self.run)["complete"])
            self.assertTrue(runner.execute(self.run)["complete"])
        self.assertEqual(len(list(self.run.glob("batches/*/attempts/*"))), 1)

    def test_offline_grok_checks_runtime_and_selection(self):
        self.prepare(provider="grok", model="grok-4.6")
        self.assertTrue(self.ingest(self.bundle(provider="grok"))["valid"])
        self.assertTrue(runner.report(self.run)["complete"])

    def test_missing_identity_input_mismatch_and_tools_fail(self):
        mutations = [lambda raw, events: events[-1]["message"].pop("model"),
                     lambda raw, events: events[0]["message"].update(content="另一个输入"),
                     lambda raw, events: events[-1]["message"]["content"].append({"type": "tool_use", "name": "x"}),
                     lambda raw, events: raw.update(stop_reason="max_tokens"),
                     lambda raw, events: raw["modelUsage"]["claude-opus-5"].update(provider="proxy")]
        for index, mutation in enumerate(mutations):
            self.run = self.root / ("run-" + str(index))
            self.prepare()
            self.assertFalse(self.ingest(self.bundle(changes=mutation))["valid"])
            self.assertFalse(runner.report(self.run)["complete"])

    def test_firstparty_auxiliary_usage_is_recorded_without_changing_primary(self):
        self.prepare()
        def add_usage(raw, events):
            raw["modelUsage"]["claude-haiku-4-5-20251001"] = dict(provider="firstParty", inputTokens=4735, outputTokens=21)
        result = self.ingest(self.bundle(changes=add_usage))
        self.assertTrue(result["valid"])
        self.assertEqual(result["identity"]["actual"], ["claude-opus-5"])
        self.assertEqual(result["identity"]["auxiliary_models"], ["claude-haiku-4-5-20251001"])
        self.assertEqual(result["identity"]["auxiliary_usage"]["claude-haiku-4-5-20251001"]["outputTokens"], 21)

    def test_auxiliary_main_message_or_non_firstparty_usage_is_rejected(self):
        for index, variant in enumerate(("main-message", "proxy-usage", "missing-token-usage")):
            self.run = self.root / ("aux-run-" + str(index))
            self.prepare()
            def mutate(raw, events):
                raw["modelUsage"]["claude-haiku-4-5-20251001"] = dict(provider="firstParty", inputTokens=10, outputTokens=21)
                if variant == "main-message":
                    events[-1]["message"]["model"] = "claude-haiku-4-5-20251001"
                elif variant == "proxy-usage":
                    raw["modelUsage"]["claude-haiku-4-5-20251001"]["provider"] = "proxy"
                else:
                    del raw["modelUsage"]["claude-haiku-4-5-20251001"]["outputTokens"]
            result = self.ingest(self.bundle(changes=mutate))
            self.assertFalse(result["valid"])
            if variant == "main-message":
                self.assertIn("claude-haiku-4-5-20251001", result["reason"])

    def test_failed_validation_can_be_rechecked_without_overwriting_or_calling(self):
        self.prepare()
        with mock.patch.object(runner, "validate_identity", side_effect=runner.RunnerError("旧验证器误拒")):
            self.assertFalse(self.ingest(self.bundle())["valid"])
        attempt = next(self.run.glob("batches/*/attempts/*"))
        original = (attempt / "validation.json").read_bytes()
        with mock.patch.object(runner.subprocess, "run", side_effect=AssertionError("禁止调用")):
            self.assertFalse(runner.resume(self.run)["complete"])
            self.assertTrue(runner.resume(self.run, revalidate_failed=True)["complete"])
            self.assertTrue(runner.resume(self.run)["complete"])
        self.assertEqual((attempt / "validation.json").read_bytes(), original)
        self.assertTrue((attempt / "revalidation-0001.json").exists())
        self.assertEqual(len(list(self.run.glob("batches/*/attempts/*"))), 1)

    def test_older_success_identity_can_gain_usage_metadata_without_regeneration(self):
        self.prepare()
        self.ingest(self.bundle())
        attempt = next(self.run.glob("batches/*/attempts/*"))
        saved = runner.read_json(attempt / "validation.json")
        for key in ("primary_usage", "auxiliary_models", "auxiliary_usage", "usage_note"):
            saved["identity"].pop(key)
        write_json(attempt / "validation.json", saved)
        original = (attempt / "validation.json").read_bytes()
        with mock.patch.object(runner.subprocess, "run", side_effect=AssertionError("禁止调用")):
            self.assertTrue(runner.resume(self.run)["complete"])
        self.assertEqual((attempt / "validation.json").read_bytes(), original)
        enriched = runner.read_json(attempt / "revalidation-0001.json")
        self.assertEqual(enriched["identity"]["auxiliary_models"], [])

    def test_failed_evidence_cannot_be_replaced_before_revalidation(self):
        self.prepare()
        with mock.patch.object(runner, "validate_identity", side_effect=runner.RunnerError("旧验证器误拒")):
            self.ingest(self.bundle())
        attempt = next(self.run.glob("batches/*/attempts/*"))
        raw = runner.read_json(attempt / "output.json")
        raw["modelUsage"]["claude-opus-5"]["inputTokens"] = 999
        write_json(attempt / "output.json", raw)
        with self.assertRaises(runner.RunnerError):
            runner.resume(self.run, revalidate_failed=True)
        self.assertFalse((attempt / "revalidation-0001.json").exists())

    def test_legacy_failure_without_hash_baseline_is_explicit(self):
        self.prepare()
        with mock.patch.object(runner, "validate_identity", side_effect=runner.RunnerError("旧验证器误拒")):
            self.ingest(self.bundle())
        attempt = next(self.run.glob("batches/*/attempts/*"))
        write_json(attempt / "validation.json", dict(valid=False, reason="没有证据hash的旧格式失败"))
        result = runner.resume(self.run, revalidate_failed=True)
        self.assertTrue(result["complete"])
        self.assertEqual(result["batches"][0]["evidence_baseline"], "legacy_failure_unavailable")

    def test_missing_grok_fingerprint_fails(self):
        self.prepare(provider="grok", model="grok-4.6")
        bundle = self.bundle(provider="grok", changes=lambda raw, events: events[-1].pop("model_fingerprint"))
        self.assertFalse(self.ingest(bundle)["valid"])

    def test_grok_selection_mismatch_and_wrong_session_path_fail(self):
        self.prepare(provider="grok", model="grok-4.6")
        bundle = self.bundle(provider="grok")
        signals = next(bundle.rglob("signals.json"))
        write_json(signals, dict(modelsUsed=["grok-other"]))
        self.assertFalse(self.ingest(bundle)["valid"])
        bundle = self.bundle(provider="grok")
        next(bundle.glob("fixture-session")).rename(bundle / "wrong-session")
        self.assertFalse(self.ingest(bundle, retry_failed=True)["valid"])

    def test_timeout_and_truncated_json_never_pass(self):
        self.prepare()
        bundle = self.bundle()
        write_json(bundle / "completion.json", {"exit_code": 0, "timed_out": True})
        self.assertFalse(self.ingest(bundle)["valid"])
        broken = self.bundle()
        (broken / "output.json").write_text('{"result":')
        self.assertFalse(self.ingest(broken, retry_failed=True)["valid"])

    def test_failure_retry_is_explicit_and_keeps_old_attempt(self):
        self.prepare()
        bad = self.bundle(answer='{"cases": []}')
        self.assertFalse(self.ingest(bad)["valid"])
        good = self.bundle()
        with self.assertRaises(runner.RunnerError):
            self.ingest(good)
        self.assertTrue(self.ingest(good, retry_failed=True)["valid"])
        self.assertEqual(len(list(self.run.glob("batches/*/attempts/*"))), 2)

    def test_budget_counts_failed_imports(self):
        self.prepare(max_calls=1)
        self.assertFalse(self.ingest(self.bundle(answer='{"cases": []}'))["valid"])
        with self.assertRaises(runner.RunnerError):
            self.ingest(self.bundle(), retry_failed=True)

    def test_pending_attempt_can_be_completed_offline_without_new_budget(self):
        self.prepare(max_calls=1)
        plan, manifest = runner.load_run(self.run)
        attempt = runner.reserve_attempt(self.run, plan, manifest, manifest["batches"][0], False, "cli")
        self.assertFalse(runner.resume(self.run)["complete"])
        self.assertFalse((attempt / "validation.json").exists())
        self.assertTrue(self.ingest(self.bundle())["valid"])
        self.assertEqual(len(list(self.run.glob("batches/*/attempts/*"))), 1)

    def test_pending_import_cannot_replace_existing_output(self):
        self.prepare()
        plan, manifest = runner.load_run(self.run)
        attempt = runner.reserve_attempt(self.run, plan, manifest, manifest["batches"][0], False, "cli")
        runner.save_new(attempt / "output.json", b'{"different": true}')
        with self.assertRaises(runner.RunnerError):
            self.ingest(self.bundle())
        self.assertEqual((attempt / "output.json").read_bytes(), b'{"different": true}')

    def test_exhausted_retry_budget_does_not_abandon_recoverable_attempt(self):
        self.prepare(max_calls=1)
        plan, manifest = runner.load_run(self.run)
        attempt = runner.reserve_attempt(self.run, plan, manifest, manifest["batches"][0], False, "cli")
        with self.assertRaises(runner.RunnerError):
            runner.reserve_attempt(self.run, plan, manifest, manifest["batches"][0], True, "cli")
        self.assertFalse((attempt / "validation.json").exists())
        self.assertTrue(self.ingest(self.bundle())["valid"])

    def test_cli_failure_stops_before_spending_next_batch(self):
        self.prepare(cases=self.plan["cases"] + [dict(id="B-02", source="原文二", request="改写")])
        with mock.patch.object(runner.subprocess, "run", return_value=subprocess.CompletedProcess([], 1)) as call:
            self.assertFalse(runner.execute(self.run)["complete"])
        self.assertEqual(call.call_count, 1)
        self.assertEqual(len(list(self.run.glob("batches/*/attempts/*"))), 1)

    def successful_cli(self, command, *, cwd, input, stdout, **kwargs):
        prompt = (cwd / "prompt.txt").read_text()
        ids = re.findall(r'"id": "(B-\d+)"', prompt)
        answer = json.dumps({"cases": [dict(id=cid, text="完整正文") for cid in ids]})
        raw = dict(subtype="success", is_error=False, stop_reason="end_turn", permission_denials=[],
                   result=answer, session_id="simulated-session", modelUsage={"claude-opus-5": {"provider": "firstParty"}})
        events = [dict(type="user", sessionId=raw["session_id"], message=dict(role="user", content=prompt)),
                  dict(type="assistant", sessionId=raw["session_id"], message=dict(role="assistant", model="claude-opus-5", content=answer))]
        transcript, _ = runner.persisted_paths(self.plan, cwd, raw)
        transcript.parent.mkdir(parents=True, exist_ok=True)
        transcript.write_text("\n".join(json.dumps(e) for e in events))
        stdout.write(json.dumps(raw).encode())
        return subprocess.CompletedProcess(command, 0)

    def test_selected_batch_and_new_call_limit(self):
        self.prepare(cases=self.plan["cases"] + [dict(id="B-02", source="原文二", request="改写"), dict(id="B-03", source="原文三", request="改写")])
        with mock.patch.object(runner.Path, "home", return_value=self.root / "home"), mock.patch.object(runner.subprocess, "run", side_effect=self.successful_cli) as call:
            first = runner.execute(self.run, batch_number=2)
            self.assertEqual([row["id"] for row in first["cases"]], ["B-02"])
            second = runner.execute(self.run, max_new_calls=1)
            self.assertEqual([row["id"] for row in second["cases"]], ["B-01", "B-02"])
            self.assertEqual(call.call_count, 2)

    def test_real_execution_timeout_is_recorded_and_does_not_continue(self):
        self.prepare(cases=self.plan["cases"] + [dict(id="B-02", source="二", request="改写")])
        with mock.patch.object(runner.subprocess, "run", side_effect=subprocess.TimeoutExpired("claude", 20)) as call:
            result = runner.execute(self.run)
        self.assertEqual(call.call_count, 1)
        self.assertFalse(result["complete"])
        completion = runner.read_json(next(self.run.glob("batches/*/attempts/*/completion.json")))
        self.assertTrue(completion["timed_out"])

    def test_judge_fail_is_valid_but_not_content_pass(self):
        self.prepare(phase="judge", protocol="shuorenhua-judge-v1", outputs={"B-01": "改文"}, rubric="分别判断")
        answer = json.dumps({"cases": [dict(id="B-01", fidelity="fail", task="pass", quality="better", evidence="输入是 2，输出是 3")]})
        self.assertTrue(self.ingest(self.bundle(answer=answer))["valid"])
        result = runner.report(self.run)
        self.assertTrue(result["complete"])
        self.assertEqual(result["content_status"], "fail")
        self.assertEqual(result["summary"]["quality"]["better"], 1)

    def test_ordinary_judge_stops_but_frozen_diagnostic_can_continue(self):
        cases = self.plan["cases"] + [dict(id="B-02", source="二", request="改写")]
        for diagnostic in (False, True):
            self.run = self.root / ("judge-" + str(diagnostic))
            self.prepare(phase="judge", protocol="shuorenhua-judge-v1", cases=cases,
                         outputs={"B-01": "一", "B-02": "二"}, rubric="分别判断", diagnostic=diagnostic)
            answer = json.dumps({"cases": [dict(id="B-01", fidelity="pass", task="review", quality="same", evidence="动作需复核")]})
            self.ingest(self.bundle(answer=answer))
            with mock.patch.object(runner.subprocess, "run", return_value=subprocess.CompletedProcess([], 1)) as call:
                result = runner.execute(self.run)
            self.assertEqual(call.call_count, 1 if diagnostic else 0)
            self.assertEqual(result["non_release"], diagnostic)
            self.assertEqual(result["content_status"], "review")

    def test_success_artifact_tamper_cannot_be_reused(self):
        self.prepare()
        self.ingest(self.bundle())
        attempt = next(self.run.glob("batches/*/attempts/*"))
        (attempt / "transcript.jsonl").write_text("{}\n")
        with self.assertRaises(runner.RunnerError):
            runner.report(self.run)

    def test_judge_report_computes_dimensions_and_missing_batch(self):
        cases = [dict(id="B-01", source="原文", request="改写"), dict(id="B-02", source="另一段", request="改写")]
        self.prepare(phase="judge", protocol="shuorenhua-judge-v1", cases=cases,
                     outputs={"B-01": "输出", "B-02": "另一输出"}, rubric="分别判三维")
        answer = json.dumps({"cases": [dict(id="B-01", fidelity="pass", task="review", quality="worse", evidence="动作需复核")]})
        self.assertTrue(self.ingest(self.bundle(answer=answer))["valid"])
        result = runner.report(self.run)
        self.assertFalse(result["complete"])
        self.assertEqual(result["missing_ids"], ["B-02"])
        self.assertIsNone(result["summary"])

    def test_subscription_env_does_not_copy_keys(self):
        env = runner.child_env({"PATH": "/bin", "ANTHROPIC_API_KEY": "secret", "XAI_API_KEY": "secret", "CLAUDECODE": "host"})
        self.assertEqual(env, {"PATH": "/bin"})

    def test_grok_command_removes_every_tool(self):
        self.prepare(provider="grok", model="grok-4.7")
        plan, _ = runner.load_run(self.run)
        command = runner.command_for(plan, self.run)
        # `--tools ""` 在 grok 1.0.41 不限制任何工具；必须收窄后再按内部 ID 全部移除，并保留 deny 兜底。
        self.assertNotIn("", command)
        self.assertEqual(command[command.index("--tools") + 1], "read_file")
        removed = command[command.index("--disallowed-tools") + 1].split(",")
        self.assertEqual(set(removed), {"read_file", "search_tool", "use_tool"})
        self.assertEqual(command[command.index("--deny") + 1], "*")

    def test_grok_env_hides_skills_and_keeps_real_grok_home(self):
        real = self.root / "real-grok"
        real.mkdir()
        link = self.root / "grok-link"
        link.symlink_to(real)
        fake = self.root / "fake-home"
        fake.mkdir()
        env = runner.grok_env(fake, {"PATH": "/bin", "HOME": "/Users/x", "GROK_HOME": str(link), "XAI_API_KEY": "secret"})
        self.assertEqual(env["HOME"], str(fake))
        # 沙箱拒绝软链形式的 GROK_HOME，必须解析成真实路径。
        self.assertEqual(env["GROK_HOME"], str(real.resolve()))
        self.assertNotIn("XAI_API_KEY", env)
        self.assertEqual((fake / ".grok").resolve(), real.resolve())

    def test_grok_env_defaults_to_home_dot_grok(self):
        home = self.root / "home"
        (home / ".grok").mkdir(parents=True)
        fake = self.root / "fake-home"
        fake.mkdir()
        env = runner.grok_env(fake, {"HOME": str(home)})
        self.assertEqual(env["GROK_HOME"], str((home / ".grok").resolve()))

    def test_grok_execution_runs_with_isolated_home_and_cleans_it_up(self):
        self.prepare(provider="grok", model="grok-4.7")
        real = self.root / "real-grok"
        (real / "sessions").mkdir(parents=True)
        seen = {}

        def fake_grok(command, *, cwd, env, **kwargs):
            seen.update(home=env["HOME"], grok_home=env["GROK_HOME"])
            self.assertTrue((Path(env["HOME"]) / ".grok").is_symlink())
            return subprocess.CompletedProcess(command, 1)

        with mock.patch.dict(runner.os.environ, {"GROK_HOME": str(real)}), \
                mock.patch.object(runner.subprocess, "run", side_effect=fake_grok):
            runner.execute(self.run)
        self.assertNotEqual(seen["home"], str(Path.home()))
        self.assertEqual(seen["grok_home"], str(real.resolve()))
        self.assertFalse(Path(seen["home"]).exists(), "临时 HOME 必须清理")
        # 清理只删软链，不能进入真实 Grok 目录。
        self.assertTrue((real / "sessions").is_dir())

    def test_claude_execution_keeps_the_real_home(self):
        seen = {}

        def fake_claude(command, *, env, **kwargs):
            seen["home"] = env.get("HOME")
            return subprocess.CompletedProcess(command, 1)

        self.prepare()
        with mock.patch.object(runner.subprocess, "run", side_effect=fake_claude):
            runner.execute(self.run)
        self.assertEqual(seen["home"], runner.os.environ.get("HOME"))


if __name__ == "__main__":
    unittest.main()
