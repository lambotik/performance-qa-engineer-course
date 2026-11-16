import re
import subprocess
from datetime import datetime
from pathlib import Path

import allure

SCENARIOS_ROOT = Path(__file__).resolve().parents[1] / "scenarios"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _report_path_from_config(config_path: Path) -> Path:
    content = config_path.read_text(encoding="utf-8")
    match = re.search(r"^html\s*=\s*(.+)\s*$", content, re.MULTILINE)
    if match:
        html_value = match.group(1).strip().strip('"').strip("'")
        path = Path(html_value)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path
    return config_path.with_name("report.html")


def _run_scenario(config_rel_path: str, title: str, description: str) -> None:
    config_path = SCENARIOS_ROOT / config_rel_path
    allure.dynamic.title(title)
    allure.dynamic.description(description)

    report_path = _report_path_from_config(config_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["locust", f"--config={config_path}", f"--html={report_path}"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    if report_path.exists():
        allure.attach.file(
            str(report_path),
            name=f"Locust report: {config_rel_path} ({datetime.today():%Y-%m-%d %H:%M:%S})",
            attachment_type=allure.attachment_type.HTML,
        )

    assert result.returncode == 0, (
        f"Locust failed for {config_rel_path} with exit code {result.returncode}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


def test_grpc_gateway_existing_user_get_documents() -> None:
    _run_scenario(
        "grpc/gateway/existing_user_get_documents/v1.0.conf",
        "gRPC Gateway: existing user get documents",
        "Нагрузочный тест gRPC gateway: получение документов существующего пользователя.",
    )


def test_grpc_gateway_existing_user_get_operations() -> None:
    _run_scenario(
        "grpc/gateway/existing_user_get_operations/v1.0.conf",
        "gRPC Gateway: existing user get operations",
        "Нагрузочный тест gRPC gateway: получение операций существующего пользователя.",
    )


def test_grpc_gateway_existing_user_make_purchase_operation() -> None:
    _run_scenario(
        "grpc/gateway/existing_user_make_purchase_operation/v1.0.conf",
        "gRPC Gateway: existing user make purchase operation",
        "Нагрузочный тест gRPC gateway: покупка существующим пользователем.",
    )


def test_grpc_gateway_new_user_get_accounts() -> None:
    _run_scenario(
        "grpc/gateway/new_user_get_accounts/v1.0.conf",
        "gRPC Gateway: new user get accounts",
        "Нагрузочный тест gRPC gateway: получение счетов нового пользователя.",
    )


def test_grpc_gateway_new_user_get_documents() -> None:
    _run_scenario(
        "grpc/gateway/new_user_get_documents/v1.0.conf",
        "gRPC Gateway: new user get documents",
        "Нагрузочный тест gRPC gateway: получение документов нового пользователя.",
    )


def test_grpc_gateway_new_user_issue_physical_card() -> None:
    _run_scenario(
        "grpc/gateway/new_user_issue_physical_card/v1.0.conf",
        "gRPC Gateway: new user issue physical card",
        "Нагрузочный тест gRPC gateway: выпуск физической карты для нового пользователя.",
    )


def test_grpc_gateway_new_user_make_top_up_operation() -> None:
    _run_scenario(
        "grpc/gateway/new_user_make_top_up_operation/v1.0.conf",
        "gRPC Gateway: new user make top up operation",
        "Нагрузочный тест gRPC gateway: пополнение счёта новым пользователем.",
    )


def test_http_gateway_existing_user_get_documents() -> None:
    _run_scenario(
        "http/gateway/existing_user_get_documents/v1.0.conf",
        "HTTP Gateway: existing user get documents",
        "Нагрузочный тест HTTP gateway: получение документов существующего пользователя.",
    )


def test_http_gateway_existing_user_get_operations() -> None:
    _run_scenario(
        "http/gateway/existing_user_get_operations/v1.0.conf",
        "HTTP Gateway: existing user get operations",
        "Нагрузочный тест HTTP gateway: получение операций существующего пользователя.",
    )


def test_http_gateway_existing_user_issue_virtual_card() -> None:
    _run_scenario(
        "http/gateway/existing_user_issue_virtual_card/v1.0.conf",
        "HTTP Gateway: existing user issue virtual card",
        "Нагрузочный тест HTTP gateway: выпуск виртуальной карты существующему пользователю.",
    )


def test_http_gateway_existing_user_make_purchase_operation() -> None:
    _run_scenario(
        "http/gateway/existing_user_make_purchase_operation/v1.0.conf",
        "HTTP Gateway: existing user make purchase operation",
        "Нагрузочный тест HTTP gateway: покупка существующим пользователем.",
    )


def test_http_gateway_new_user_get_accounts() -> None:
    _run_scenario(
        "http/gateway/new_user_get_accounts/v1.0.conf",
        "HTTP Gateway: new user get accounts",
        "Нагрузочный тест HTTP gateway: получение счетов нового пользователя.",
    )


def test_http_gateway_new_user_get_documents() -> None:
    _run_scenario(
        "http/gateway/new_user_get_documents/v1.0.conf",
        "HTTP Gateway: new user get documents",
        "Нагрузочный тест HTTP gateway: получение документов нового пользователя.",
    )


def test_http_gateway_new_user_issue_physical_card() -> None:
    _run_scenario(
        "http/gateway/new_user_issue_physical_card/v1.0.conf",
        "HTTP Gateway: new user issue physical card",
        "Нагрузочный тест HTTP gateway: выпуск физической карты для нового пользователя.",
    )


def test_http_gateway_new_user_make_top_up_operation() -> None:
    _run_scenario(
        "http/gateway/new_user_make_top_up_operation/v1.0.conf",
        "HTTP Gateway: new user make top up operation",
        "Нагрузочный тест HTTP gateway: пополнение счёта новым пользователем.",
    )
