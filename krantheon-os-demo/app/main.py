import hashlib
import json
import random
import re
import time
from enum import Enum
from typing import Dict, List, Optional

from fastapi import FastAPI
from fastapi import FastAPI

app = FastAPI(title="Krantheon OS Demo API v1.0")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Krantheon OS Demo API running."}

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------------------------------------------------------
#  Krantheon OS Demo API - Deterministic, Copy-Paste Ready
# ---------------------------------------------------------

app = FastAPI(title="Krantheon OS Demo API v1.0")

# Allow all origins for easy front-end integration (Wix, local, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
#  Models
# -----------------------------

class CommandType(str, Enum):
    INVESTIGATE_IP = "investigate_ip"
    SHOW_ALERTS = "show_alerts"
    RISK_SCORE = "risk_score"
    COMPLIANCE_REPORT = "compliance_report"
    UNKNOWN = "unknown"


class CommandInput(BaseModel):
    command: str
    session_id: Optional[str] = "demo"


class RoutedCommand(BaseModel):
    command: CommandType
    confidence: float
    params: Dict[str, str]
    raw: str


# -----------------------------
#  Deterministic Router
# -----------------------------

def route_command(transcript: str) -> RoutedCommand:
    """
    100% deterministic, regex-based routing.
    No external calls. Same input → same output.
    """
    text = transcript.strip().lower()

    # INVESTIGATE IP
    m = re.search(
        r"(?:investigate|check|analyze|look\s+up)\s+(?:ip\s+)?"
        r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
        text,
    )
    if m:
        return RoutedCommand(
            command=CommandType.INVESTIGATE_IP,
            confidence=0.95,
            params={"ip": m.group("ip")},
            raw=transcript,
        )

    # SHOW ALERTS
    m = re.search(
        r"(?:show|display|list|get)\s+(?P<severity>critical|high|medium|low|all)?"
        r"\s*(alerts|notifications)",
        text,
    )
    if m:
        severity = m.group("severity") or "critical"
        return RoutedCommand(
            command=CommandType.SHOW_ALERTS,
            confidence=0.9,
            params={"severity": severity},
            raw=transcript,
        )

    # RISK SCORE
    m = re.search(
        r"(?:risk\s+score|score)\s+(?:for\s+)?"
        r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})?",
        text,
    )
    if m:
        ip = m.group("ip") or "1.1.1.1"
        return RoutedCommand(
            command=CommandType.RISK_SCORE,
            confidence=0.9,
            params={"ip": ip},
            raw=transcript,
        )

    # COMPLIANCE REPORT
    if re.search(r"(compliance|audit)\s+(report|status|check)", text):
        return RoutedCommand(
            command=CommandType.COMPLIANCE_REPORT,
            confidence=0.9,
            params={},
            raw=transcript,
        )

    # Unknown
    return RoutedCommand(
        command=CommandType.UNKNOWN,
        confidence=0.0,
        params={},
        raw=transcript,
    )


# -----------------------------
#  Engines (Deterministic, demo)
# -----------------------------

def deterministic_hash(data: Dict) -> str:
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def investigate_ip(ip: str) -> Dict:
    last_octet = int(ip.split(".")[-1])
    risk = round((last_octet % 10) / 10.0, 2)
    threats = last_octet % 5
    return {
        "ip": ip,
        "risk_score": risk,
        "threats_detected": threats,
        "summary": f"IP {ip} analyzed. {threats} threat indicators. Risk {risk}.",
    }


def show_alerts(severity: str) -> Dict:
    base = {"critical": 7, "high": 12, "medium": 18, "low": 4, "all": 37}
    count = base.get(severity, 7)
    return {
        "severity": severity,
        "active_alerts": count,
        "summary": f"{severity.title()} alerts: {count} active.",
    }


def risk_score(ip: str) -> Dict:
    last_octet = int(ip.split(".")[-1])
    score = round((last_octet % 7) / 10.0 + 0.3, 2)
    level = "low"
    if score >= 0.8:
        level = "critical"
    elif score >= 0.6:
        level = "high"
    elif score >= 0.4:
        level = "medium"
    return {
        "ip": ip,
        "score": score,
        "level": level,
        "summary": f"Risk score for {ip}: {score} ({level}).",
    }


def compliance_report() -> Dict:
    return {
        "soc2_policies_total": 247,
        "soc2_policies_passed": 247,
        "suspensions": 0,
        "summary": "Compliance 100%. 247 SOC2 policies passed. 0 suspensions.",
    }


def agency_dashboard_data() -> Dict:
    return {
        "suspensions": 0,
        "tickets_resolved_pct": 95,
        "clv_usd": 47000,
        "roas": 4.2,
        "campaigns_active": 23,
        "summary": "Agency: 4.2x ROAS, 0 suspensions, 95% tickets auto-resolved.",
    }


def athlete_hub_data() -> Dict:
    return {
        "athletes": [
            {
                "id": "ath-1",
                "name": "Sarah Swift",
                "sport": "Track",
                "monthly_rate": 2500,
                "predicted_ctr": 0.023,
            },
            {
                "id": "ath-2",
                "name": "Mike Thunder",
                "sport": "Basketball",
                "monthly_rate": 4500,
                "predicted_ctr": 0.031,
            },
        ],
        "summary": "Athlete hub: 2 featured talents with live CTR predictions.",
    }


def hca_registry_data() -> Dict:
    return {
        "total_assets": 5600000,
        "enterprise_value": 49300000,
        "defi_collateral": 25600000,
        "hca_tokens": 430000,
        "summary": "HCA Registry: 5.6M assets, $49.3M enterprise value, $25.6M DeFi collateral.",
    }


def campaigns_data() -> Dict:
    return {
        "active": 12,
        "budget_usd": 284000,
        "roas": 3.8,
        "platforms": ["Google", "Meta", "TikTok", "Reddit"],
        "summary": "12 active campaigns, $284K budget, 3.8x blended ROAS.",
    }


# -----------------------------
#  API Endpoints
# -----------------------------

@app.post("/api/command")
async def api_command(cmd: CommandInput):
    """
    Main voice/command endpoint.
    Handles:
    - investigate 8.8.8.8
    - show critical alerts
    - risk score 1.1.1.1
    - compliance report
    """
    start = time.time()
    routed = route_command(cmd.command)

    if routed.command == CommandType.INVESTIGATE_IP:
        out = investigate_ip(routed.params["ip"])
    elif routed.command == CommandType.SHOW_ALERTS:
        out = show_alerts(routed.params["severity"])
    elif routed.command == CommandType.RISK_SCORE:
        out = risk_score(routed.params["ip"])
    elif routed.command == CommandType.COMPLIANCE_REPORT:
        out = compliance_report()
    else:
        out = {
            "summary": "Command not recognized. Try: 'investigate 8.8.8.8', 'show critical alerts', 'risk score 1.1.1.1', or 'compliance report'."
        }

    latency_ms = int((time.time() - start) * 1000)
    audit = {
        "command": routed.command.value,
        "confidence": routed.confidence,
        "params": routed.params,
        "output": out,
        "session_id": cmd.session_id,
        "latency_ms": latency_ms,
    }
    audit_hash = deterministic_hash(audit)

    return {
        "success": True,
        "command": routed.command.value,
        "confidence": routed.confidence,
        "params": routed.params,
        "response": out["summary"],
        "data": out,
        "audit_hash": audit_hash[:16],
        "latency_ms": latency_ms,
        "session_id": cmd.session_id,
    }


@app.get("/api/agency")
async def api_agency():
    data = agency_dashboard_data()
    return {
        "success": True,
        "data": data,
        "audit_hash": deterministic_hash(data)[:16],
    }


@app.get("/api/athletes")
async def api_athletes():
    data = athlete_hub_data()
    return {
        "success": True,
        "data": data,
        "audit_hash": deterministic_hash(data)[:16],
    }


@app.get("/api/hca")
async def api_hca():
    data = hca_registry_data()
    return {
        "success": True,
        "data": data,
        "audit_hash": deterministic_hash(data)[:16],
    }


@app.get("/api/campaigns")
async def api_campaigns():
    data = campaigns_data()
    return {
        "success": True,
        "data": data,
        "audit_hash": deterministic_hash(data)[:16],
    }


@app.get("/")
async def root():
    return {"status": "ok", "message": "Krantheon OS Demo API running."}
