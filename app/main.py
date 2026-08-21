# ============================================================
# STANDARD LIBRARY
# ============================================================

import sys
from pathlib import Path
from datetime import date, time


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Make the project root available to Python
# before importing the services package.

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
import plotly.graph_objects as go

from services.fortyguard import FortyGuardClient
from services.thermal_analyzer import ThermalAnalyzer
from services.operations_recommender import OperationsRecommender


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="THERMALYTIC AI",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HTML RENDER HELPER
# ============================================================

def render_html(content):
    st.html(content)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 12% 4%,
                rgba(35, 115, 255, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 92% 8%,
                rgba(255, 95, 55, 0.08),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #07101b 0%,
                #0b1422 48%,
                #09111c 100%
            );

        color: #f4f7fb;
    }

    .block-container {
        max-width: 1480px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 42px 46px;
        margin-bottom: 32px;

        border-radius: 28px;

        background:
            linear-gradient(
                135deg,
                rgba(16, 34, 58, 0.97),
                rgba(11, 22, 37, 0.97)
            );

        border: 1px solid rgba(150, 190, 230, 0.12);

        box-shadow:
            0 24px 70px rgba(0, 0, 0, 0.35),
            inset 0 1px 0 rgba(255,255,255,0.05);
    }

    .hero::before {
        content: "";

        position: absolute;

        width: 420px;
        height: 420px;

        right: -150px;
        top: -240px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(255, 103, 55, 0.16),
                transparent 68%
            );

        filter: blur(25px);

        animation: softGlow 7s ease-in-out infinite;
    }

    .hero-content {
        position: relative;
        z-index: 2;
    }

    .hero-kicker {
        display: inline-block;

        margin-bottom: 15px;

        padding: 7px 12px;

        border-radius: 999px;

        border: 1px solid rgba(87, 183, 255, 0.20);

        background: rgba(87, 183, 255, 0.07);

        color: #8ecbff;

        font-size: 11px;

        font-weight: 700;

        letter-spacing: 1.4px;

        text-transform: uppercase;
    }

    .hero-title {
        margin: 0;

        font-size: 52px;

        line-height: 1.05;

        font-weight: 900;

        letter-spacing: -2px;

        color: #f8fbff;
    }

    .hero-title span {
        color: #ff8057;
    }

    .hero-subtitle {
        margin-top: 13px;

        max-width: 780px;

        font-size: 18px;

        line-height: 1.6;

        color: #aebbd0;
    }

    .hero-status {
        display: inline-flex;

        align-items: center;

        gap: 8px;

        margin-top: 22px;

        padding: 8px 13px;

        border-radius: 999px;

        background: rgba(35, 203, 135, 0.07);

        border: 1px solid rgba(35, 203, 135, 0.18);

        color: #5fe0a6;

        font-size: 12px;

        font-weight: 700;

        letter-spacing: 0.5px;
    }

    .status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #42d995;

        box-shadow:
            0 0 12px rgba(66, 217, 149, 0.7);
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        margin-top: 34px;
        margin-bottom: 7px;

        font-size: 26px;

        line-height: 1.2;

        font-weight: 850;

        color: #f4f7fb;

        letter-spacing: -0.5px;
    }

    .section-subtitle {
        margin-bottom: 18px;

        color: #8290a5;

        font-size: 14px;

        line-height: 1.6;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    .metric-card {
        position: relative;

        min-height: 150px;

        padding: 24px;

        overflow: hidden;

        border-radius: 20px;

        background:
            linear-gradient(
                145deg,
                rgba(22, 36, 55, 0.94),
                rgba(12, 23, 38, 0.94)
            );

        border: 1px solid rgba(150, 190, 230, 0.10);

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.22),
            inset 0 1px 0 rgba(255,255,255,0.04);

        transition:
            transform 0.22s ease,
            border-color 0.22s ease,
            box-shadow 0.22s ease;
    }

    .metric-card::after {
        content: "";

        position: absolute;

        width: 120px;
        height: 120px;

        right: -60px;
        top: -60px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(71, 154, 255, 0.08),
                transparent 70%
            );
    }

    .metric-card:hover {
        transform: translateY(-4px);

        border-color:
            rgba(104, 177, 255, 0.22);

        box-shadow:
            0 20px 50px rgba(0, 0, 0, 0.30),
            0 0 24px rgba(70, 150, 255, 0.05);
    }

    .metric-label {
        position: relative;
        z-index: 2;

        color: #8391a6;

        font-size: 12px;

        font-weight: 750;

        letter-spacing: 1px;

        text-transform: uppercase;
    }

    .metric-value {
        position: relative;
        z-index: 2;

        margin-top: 10px;

        font-size: 34px;

        line-height: 1.1;

        font-weight: 900;

        color: #f8fbff;
    }

    .metric-small {
        position: relative;
        z-index: 2;

        margin-top: 8px;

        color: #69788e;

        font-size: 12px;
    }


    /* ========================================================
       OPERATIONAL RECOMMENDATION
       ======================================================== */

    .recommendation-card {
        position: relative;

        overflow: hidden;

        padding: 28px 30px;

        margin-bottom: 12px;

        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(18, 31, 48, 0.98),
                rgba(12, 22, 36, 0.98)
            );

        border: 1px solid rgba(150, 190, 230, 0.12);

        box-shadow:
            0 18px 48px rgba(0, 0, 0, 0.25);
    }

    .recommendation-card::before {
        content: "";

        position: absolute;

        left: 0;
        top: 0;
        bottom: 0;

        width: 4px;

        background: #e6b94a;
    }

    .recommendation-header {
        display: flex;

        align-items: center;

        justify-content: space-between;
    }

    .recommendation-label {
        color: #718096;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 1.2px;
    }

    .recommendation-priority {
        margin-top: 5px;

        font-size: 25px;

        font-weight: 900;

        color: #e6b94a;
    }

    .recommendation-main {
        margin-top: 22px;

        padding: 18px 20px;

        border-radius: 14px;

        background:
            rgba(255, 255, 255, 0.035);

        color: #f1f5f9;

        font-size: 18px;

        font-weight: 700;

        line-height: 1.55;
    }

    .recommendation-grid {
        display: grid;

        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 14px;

        margin-top: 14px;
    }

    .recommendation-item {
        padding: 18px;

        border-radius: 14px;

        background:
            rgba(255, 255, 255, 0.025);

        border:
            1px solid rgba(255, 255, 255, 0.055);
    }

    .recommendation-item-label {
        color: #7f8da2;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 1px;

        text-transform: uppercase;
    }

    .recommendation-item-text {
        margin-top: 8px;

        color: #b8c4d5;

        font-size: 14px;

        line-height: 1.65;
    }

    @media (max-width: 800px) {

        .recommendation-grid {
            grid-template-columns: 1fr;
        }
    }


    /* ========================================================
       RISK CARD
       ======================================================== */

    .risk-card {
        position: relative;

        overflow: hidden;

        padding: 27px 30px;

        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(126, 93, 20, 0.20),
                rgba(33, 29, 25, 0.88)
            );

        border:
            1px solid rgba(240, 190, 70, 0.18);

        box-shadow:
            0 18px 45px rgba(0, 0, 0, 0.25);
    }

    .risk-card.high {
        border-color:
            rgba(255, 80, 80, 0.25);
    }

    .risk-title {
        font-size: 25px;

        font-weight: 900;

        color: #ffd66b;
    }

    .risk-description {
        margin-top: 9px;

        max-width: 900px;

        color: #abb5c5;

        line-height: 1.7;

        font-size: 14px;
    }


    /* ========================================================
       HOTSPOT CARD
       ======================================================== */

    .hotspot-card {
        padding: 18px 20px;

        margin-bottom: 10px;

        border-radius: 16px;

        background:
            rgba(26, 31, 42, 0.85);

        border:
            1px solid rgba(255, 100, 70, 0.14);

        color: #dce4ef;

        transition:
            transform 0.18s ease,
            border-color 0.18s ease;
    }

    .hotspot-card:hover {
        transform: translateX(4px);

        border-color:
            rgba(255, 100, 70, 0.30);
    }


    /* ========================================================
       SYSTEM STATUS
       ======================================================== */

    .system-card {
        padding: 18px 25px;

        border-radius: 20px;

        background:
            rgba(14, 24, 39, 0.88);

        border:
            1px solid rgba(150, 190, 230, 0.09);

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.22);
    }

    .system-row {
        display: flex;

        justify-content: space-between;

        align-items: center;

        padding: 16px 3px;

        border-bottom:
            1px solid rgba(255,255,255,0.055);
    }

    .system-row:last-child {
        border-bottom: none;
    }

    .system-name {
        color: #b5c1d2;

        font-size: 14px;

        font-weight: 600;
    }

    .system-status {
        color: #54d99a;

        font-size: 12px;

        font-weight: 800;

        letter-spacing: 0.7px;
    }


    /* ========================================================
       RUN BUTTON
       ======================================================== */

    div.stButton > button {
        width: 100%;

        min-height: 56px;

        border-radius: 15px;

        border: 1px solid rgba(255, 137, 91, 0.28);

        background:
            linear-gradient(
                135deg,
                #e95735,
                #c83e2c
            );

        color: white;

        font-size: 15px;

        font-weight: 800;

        letter-spacing: 0.2px;

        box-shadow:
            0 10px 28px rgba(207, 66, 43, 0.22);

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            filter 0.18s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);

        filter: brightness(1.06);

        box-shadow:
            0 15px 35px rgba(207, 66, 43, 0.32);
    }

    div.stButton > button:active {
        transform: translateY(0);
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07101b,
                #091522
            );

        border-right:
            1px solid rgba(150,190,230,0.08);
    }

    [data-testid="stSidebar"] h2 {
        color: #edf3fa;
    }

    [data-testid="stSidebar"] h3 {
        color: #8393a9;

        font-size: 11px;

        letter-spacing: 1.2px;

        text-transform: uppercase;
    }

    [data-testid="stSidebar"] p {
        color: #a4b1c2;
    }


    /* ========================================================
       STREAMLIT ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 15px;
    }


    /* ========================================================
       PLOTLY CONTAINER
       ======================================================== */

    [data-testid="stPlotlyChart"] {
        border-radius: 20px;

        overflow: hidden;

        border:
            1px solid rgba(150,190,230,0.08);

        box-shadow:
            0 18px 45px rgba(0,0,0,0.25);
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        margin-top: 60px;

        padding-top: 24px;

        text-align: center;

        border-top:
            1px solid rgba(255,255,255,0.06);

        color: #5f6d80;

        font-size: 12px;

        line-height: 1.8;
    }


    /* ========================================================
       ANIMATION
       ======================================================== */

    @keyframes softGlow {

        0%, 100% {
            transform: scale(1);
            opacity: 0.65;
        }

        50% {
            transform: scale(1.08);
            opacity: 0.9;
        }
    }


    /* ========================================================
       REDUCE MOTION
       ======================================================== */

    @media (prefers-reduced-motion: reduce) {

        *,
        *::before,
        *::after {
            animation: none !important;
            transition: none !important;
        }
    }


    /* ========================================================
       PREMIUM MOTION + VISUAL POLISH
       ======================================================== */

    html {
        scroll-behavior: smooth;
    }

    .hero {
        animation: heroIn 0.75s cubic-bezier(.2,.8,.2,1) both;
    }

    .hero::after {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background:
            linear-gradient(
                115deg,
                transparent 0%,
                rgba(255,255,255,0.035) 42%,
                transparent 55%
            );
        transform: translateX(-120%);
        animation: heroSweep 8s ease-in-out infinite;
    }

    .status-dot {
        animation: statusPulse 1.8s ease-in-out infinite;
    }

    .metric-card {
        animation: cardIn 0.65s cubic-bezier(.2,.8,.2,1) both;
        will-change: transform;
    }

    .metric-card:nth-child(2) {
        animation-delay: 0.06s;
    }

    .metric-card:nth-child(3) {
        animation-delay: 0.12s;
    }

    .metric-card:nth-child(4) {
        animation-delay: 0.18s;
    }

    .metric-value {
        text-shadow: 0 0 22px rgba(110, 190, 255, 0.08);
    }

    .recommendation-card {
        animation: cardIn 0.7s cubic-bezier(.2,.8,.2,1) both;
    }

    .recommendation-main {
        position: relative;
        overflow: hidden;
    }

    .recommendation-main::after {
        content: "";
        position: absolute;
        top: 0;
        bottom: 0;
        width: 90px;
        left: -120px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.08),
            transparent
        );
        transform: skewX(-18deg);
        animation: recommendationSweep 5s ease-in-out infinite;
    }

    .risk-card {
        animation: riskIn 0.7s cubic-bezier(.2,.8,.2,1) both;
    }

    .risk-card::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        right: -130px;
        bottom: -160px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            rgba(255, 190, 70, 0.11),
            transparent 70%
        );
        animation: riskGlow 4s ease-in-out infinite;
    }

    .hotspot-card {
        animation: slideIn 0.5s cubic-bezier(.2,.8,.2,1) both;
    }

    .system-card {
        animation: cardIn 0.7s cubic-bezier(.2,.8,.2,1) both;
    }

    .system-status {
        display: inline-flex;
        align-items: center;
        gap: 7px;
    }

    .system-status::before {
        content: "";
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #54d99a;
        box-shadow: 0 0 10px rgba(84, 217, 154, 0.65);
        animation: statusPulse 2s ease-in-out infinite;
    }

    div.stButton > button {
        position: relative;
        overflow: hidden;
        background-size: 200% 200%;
        animation: buttonGradient 5s ease infinite;
    }

    div.stButton > button::after {
        content: "";
        position: absolute;
        top: -40%;
        left: -80%;
        width: 45%;
        height: 180%;
        transform: rotate(18deg);
        background: rgba(255,255,255,0.12);
        animation: buttonSweep 4.5s ease-in-out infinite;
    }

    [data-testid="stPlotlyChart"] {
        animation: chartIn 0.9s cubic-bezier(.2,.8,.2,1) both;
    }

    .footer {
        animation: fadeIn 1s ease both;
    }

    @keyframes heroIn {
        from {
            opacity: 0;
            transform: translateY(18px) scale(0.985);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes cardIn {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes riskIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes chartIn {
        from {
            opacity: 0;
            transform: scale(0.985);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes statusPulse {
        0%, 100% {
            transform: scale(1);
            opacity: 0.75;
        }
        50% {
            transform: scale(1.25);
            opacity: 1;
        }
    }

    @keyframes heroSweep {
        0%, 35% {
            transform: translateX(-120%);
        }
        60%, 100% {
            transform: translateX(120%);
        }
    }

    @keyframes recommendationSweep {
        0%, 55% {
            left: -120px;
        }
        75%, 100% {
            left: 115%;
        }
    }

    @keyframes riskGlow {
        0%, 100% {
            transform: scale(1);
            opacity: 0.55;
        }
        50% {
            transform: scale(1.15);
            opacity: 0.95;
        }
    }

    @keyframes buttonGradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    @keyframes buttonSweep {
        0%, 55% {
            left: -80%;
        }
        75%, 100% {
            left: 130%;
        }
    }

    /* Improve input controls so the planning area feels like one
       coherent operational console. */
    [data-testid="stSelectbox"],
    [data-testid="stDateInput"],
    [data-testid="stTimeInput"],
    [data-testid="stNumberInput"] {
        transition: transform 0.2s ease, filter 0.2s ease;
    }

    [data-testid="stSelectbox"]:focus-within,
    [data-testid="stDateInput"]:focus-within,
    [data-testid="stTimeInput"]:focus-within,
    [data-testid="stNumberInput"]:focus-within {
        transform: translateY(-1px);
        filter: brightness(1.04);
    }

    /* Cleaner Streamlit chrome for the final demo. */
    header[data-testid="stHeader"] {
        background: rgba(7, 16, 27, 0.55);
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    /* Keep animations accessible. */
    @media (prefers-reduced-motion: reduce) {
        html {
            scroll-behavior: auto;
        }

        .hero,
        .metric-card,
        .recommendation-card,
        .risk-card,
        .hotspot-card,
        .system-card,
        [data-testid="stPlotlyChart"],
        .footer {
            animation: none !important;
        }

        .hero::after,
        .recommendation-main::after,
        .risk-card::after,
        div.stButton > button::after {
            display: none !important;
        }
    }


    /* ========================================================
       CREATIVE THERMAL INTELLIGENCE ANIMATION PACK 2.0
       ======================================================== */

    .hero {
        animation: heroEnter 0.9s cubic-bezier(.2,.8,.2,1) both;
    }

    .hero::after {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background:
            linear-gradient(
                115deg,
                transparent 0%,
                rgba(255,255,255,0.00) 38%,
                rgba(255,140,80,0.08) 48%,
                rgba(255,255,255,0.00) 58%,
                transparent 100%
            );
        transform: translateX(-120%);
        animation: thermalSweep 7s ease-in-out infinite;
    }

    .hero-status {
        position: relative;
        overflow: hidden;
    }

    .hero-status::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(95,224,166,0.16),
            transparent
        );
        transform: translateX(-100%);
        animation: statusSweep 3.8s linear infinite;
    }

    .status-dot {
        animation: statusPulse 1.8s ease-in-out infinite;
    }

    .metric-card {
        animation: cardReveal 0.65s cubic-bezier(.2,.8,.2,1) both;
    }

    .metric-card:nth-child(2) {
        animation-delay: .08s;
    }

    .metric-card:nth-child(3) {
        animation-delay: .16s;
    }

    .metric-card:nth-child(4) {
        animation-delay: .24s;
    }

    .metric-value {
        text-shadow: 0 0 24px rgba(100,180,255,0.10);
    }

    .risk-card {
        animation: riskReveal 0.8s cubic-bezier(.2,.8,.2,1) both;
    }

    .risk-card::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        right: -130px;
        top: -130px;
        border-radius: 50%;
        border: 1px solid rgba(255,214,107,0.10);
        box-shadow:
            0 0 0 22px rgba(255,214,107,0.025),
            0 0 0 44px rgba(255,214,107,0.018);
        animation: riskOrbit 8s linear infinite;
        pointer-events: none;
    }

    .recommendation-card {
        animation: recommendationEnter 0.85s cubic-bezier(.2,.8,.2,1) both;
    }

    .recommendation-card::after {
        content: "";
        position: absolute;
        top: 0;
        bottom: 0;
        width: 2px;
        left: -20%;
        background: linear-gradient(
            180deg,
            transparent,
            rgba(255,214,107,0.65),
            transparent
        );
        filter: blur(1px);
        animation: recommendationScan 4.5s ease-in-out infinite;
    }

    .recommendation-main {
        position: relative;
        overflow: hidden;
    }

    .recommendation-main::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(
            105deg,
            transparent 20%,
            rgba(255,255,255,0.055) 48%,
            transparent 76%
        );
        transform: translateX(-120%);
        animation: contentShimmer 5.5s ease-in-out infinite;
    }

    .hotspot-card {
        animation: hotspotReveal 0.55s cubic-bezier(.2,.8,.2,1) both;
    }

    .hotspot-card::before {
        content: "";
        display: inline-block;
        width: 7px;
        height: 7px;
        margin-right: 10px;
        border-radius: 50%;
        background: #ff7657;
        box-shadow: 0 0 0 rgba(255,118,87,0.0);
        animation: hotspotPulse 2s ease-in-out infinite;
        vertical-align: middle;
    }

    [data-testid="stPlotlyChart"] {
        animation: chartReveal 1s cubic-bezier(.2,.8,.2,1) both;
    }

    .system-card {
        animation: cardReveal 0.9s cubic-bezier(.2,.8,.2,1) both;
    }

    .system-status {
        position: relative;
    }

    .system-status::before {
        content: "";
        display: inline-block;
        width: 6px;
        height: 6px;
        margin-right: 7px;
        border-radius: 50%;
        background: #54d99a;
        box-shadow: 0 0 10px rgba(84,217,154,0.55);
        animation: systemPulse 2s ease-in-out infinite;
    }

    div.stButton > button {
        position: relative;
        overflow: hidden;
    }

    div.stButton > button::before {
        content: "";
        position: absolute;
        top: 0;
        bottom: 0;
        left: -35%;
        width: 30%;
        transform: skewX(-20deg);
        background: rgba(255,255,255,0.13);
        animation: buttonSweep 3.8s ease-in-out infinite;
    }

    .section-title {
        animation: sectionRise 0.7s cubic-bezier(.2,.8,.2,1) both;
    }

    .section-subtitle {
        animation: sectionRise 0.8s cubic-bezier(.2,.8,.2,1) both;
        animation-delay: .06s;
    }

    @keyframes heroEnter {
        from {
            opacity: 0;
            transform: translateY(18px) scale(.985);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes thermalSweep {
        0%, 18% {
            transform: translateX(-120%);
        }
        42%, 100% {
            transform: translateX(120%);
        }
    }

    @keyframes statusSweep {
        0%, 45% {
            transform: translateX(-100%);
        }
        70%, 100% {
            transform: translateX(100%);
        }
    }

    @keyframes statusPulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 0 8px rgba(66,217,149,0.45);
        }
        50% {
            transform: scale(1.35);
            box-shadow:
                0 0 8px rgba(66,217,149,0.55),
                0 0 22px rgba(66,217,149,0.35);
        }
    }

    @keyframes cardReveal {
        from {
            opacity: 0;
            transform: translateY(16px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes riskReveal {
        from {
            opacity: 0;
            transform: translateY(20px) scale(.985);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes riskOrbit {
        from {
            transform: rotate(0deg) scale(1);
        }
        50% {
            transform: rotate(180deg) scale(1.05);
        }
        to {
            transform: rotate(360deg) scale(1);
        }
    }

    @keyframes recommendationEnter {
        from {
            opacity: 0;
            transform: translateX(-18px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes recommendationScan {
        0%, 20% {
            left: -20%;
        }
        65%, 100% {
            left: 120%;
        }
    }

    @keyframes contentShimmer {
        0%, 45% {
            transform: translateX(-120%);
        }
        72%, 100% {
            transform: translateX(120%);
        }
    }

    @keyframes hotspotReveal {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes hotspotPulse {
        0%, 100% {
            box-shadow: 0 0 0 rgba(255,118,87,0);
        }
        50% {
            box-shadow:
                0 0 12px rgba(255,118,87,0.55),
                0 0 22px rgba(255,118,87,0.18);
        }
    }

    @keyframes chartReveal {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes systemPulse {
        0%, 100% {
            opacity: .65;
            transform: scale(.9);
        }
        50% {
            opacity: 1;
            transform: scale(1.15);
        }
    }

    @keyframes buttonSweep {
        0%, 42% {
            left: -35%;
        }
        68%, 100% {
            left: 125%;
        }
    }

    @keyframes sectionRise {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .hero,
        .hero::after,
        .hero-status::before,
        .status-dot,
        .metric-card,
        .risk-card,
        .risk-card::after,
        .recommendation-card,
        .recommendation-card::after,
        .recommendation-main::after,
        .hotspot-card,
        .hotspot-card::before,
        [data-testid="stPlotlyChart"],
        .system-card,
        .system-status::before,
        div.stButton > button::before,
        .section-title,
        .section-subtitle {
            animation: none !important;
        }
    }


    /* ========================================================
       THERMALYTIC AI — COMMAND CENTER VISUAL SYSTEM
       Premium thermal intelligence / cinematic dashboard layer
       ======================================================== */

    .stApp {
        background:
            radial-gradient(circle at 18% 8%, rgba(38, 137, 255, .12), transparent 28%),
            radial-gradient(circle at 82% 12%, rgba(255, 94, 53, .10), transparent 30%),
            radial-gradient(circle at 50% 90%, rgba(111, 66, 193, .08), transparent 32%),
            #060d16;
        background-attachment: fixed;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        opacity: .18;
        background-image:
            linear-gradient(rgba(105,170,220,.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(105,170,220,.035) 1px, transparent 1px);
        background-size: 44px 44px;
        mask-image: linear-gradient(to bottom, black, transparent 85%);
        animation: commandGrid 18s linear infinite;
    }

    .block-container {
        position: relative;
        z-index: 1;
    }

    .hero {
        min-height: 360px;
        display: flex;
        align-items: center;
        border-radius: 30px;
        background:
            radial-gradient(circle at 82% 42%, rgba(255,96,54,.18), transparent 20%),
            radial-gradient(circle at 72% 65%, rgba(33,155,255,.13), transparent 28%),
            linear-gradient(135deg, rgba(13,31,52,.98), rgba(6,16,28,.98));
        box-shadow:
            0 30px 90px rgba(0,0,0,.42),
            inset 0 1px 0 rgba(255,255,255,.07);
    }

    .hero::before {
        width: 620px;
        height: 620px;
        right: -170px;
        top: -150px;
        background:
            conic-gradient(
                from 0deg,
                transparent,
                rgba(255,111,67,.18),
                transparent 30%,
                rgba(66,163,255,.11),
                transparent 58%
            );
        filter: blur(24px);
        animation: thermalAurora 12s linear infinite;
    }

    .hero-content {
        max-width: 820px;
    }

    .hero-title {
        font-size: clamp(46px, 6vw, 76px);
        text-shadow:
            0 0 35px rgba(255,112,73,.10),
            0 8px 30px rgba(0,0,0,.25);
    }

    .hero-title span {
        background: linear-gradient(100deg, #ff6847, #ffb05e, #ff6847);
        background-size: 200% auto;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: heatText 5s linear infinite;
    }

    .hero-kicker {
        box-shadow: 0 0 24px rgba(82,174,255,.07);
    }

    .hero-status {
        box-shadow:
            0 0 25px rgba(66,217,149,.06),
            inset 0 0 18px rgba(66,217,149,.025);
    }

    /* Floating thermal orbs */
    .hero-content::after {
        content: "THERMAL  •  AI  •  RISK  •  DECISION";
        position: absolute;
        right: -420px;
        bottom: -110px;
        width: 520px;
        height: 520px;
        border: 1px solid rgba(91,171,255,.09);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(150,195,235,.16);
        font-size: 10px;
        letter-spacing: 4px;
        transform: rotate(-18deg);
        box-shadow:
            inset 0 0 70px rgba(54,144,255,.04),
            0 0 80px rgba(54,144,255,.04);
        animation: commandOrb 18s linear infinite;
        pointer-events: none;
    }

    /* Section glass */
    .metric-card,
    .recommendation-card,
    .risk-card,
    .system-card {
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
    }

    .metric-card {
        background:
            linear-gradient(145deg, rgba(21,39,61,.80), rgba(8,20,34,.82));
        box-shadow:
            0 20px 55px rgba(0,0,0,.26),
            inset 0 1px 0 rgba(255,255,255,.045);
    }

    .metric-card:hover {
        transform: translateY(-7px) scale(1.012);
        box-shadow:
            0 26px 65px rgba(0,0,0,.34),
            0 0 32px rgba(69,151,255,.08);
    }

    /* Temperature spectrum ribbon */
    .metric-card::before {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 2px;
        background: linear-gradient(
            90deg,
            #243cff 0%,
            #1dc6d8 25%,
            #44dc87 42%,
            #e4dc4d 58%,
            #ff9348 76%,
            #ff4d4d 100%
        );
        background-size: 180% 100%;
        opacity: .55;
        animation: spectrumMove 6s linear infinite;
    }

    /* Risk card as a command alert */
    .risk-card {
        background:
            radial-gradient(circle at 88% 20%, rgba(255,196,68,.11), transparent 26%),
            linear-gradient(135deg, rgba(75,58,20,.32), rgba(13,24,37,.92));
    }

    .risk-title {
        letter-spacing: .5px;
        text-shadow: 0 0 20px rgba(255,214,107,.10);
    }

    /* Decision/recommendation command console */
    .recommendation-card {
        background:
            radial-gradient(circle at 100% 0%, rgba(255,180,68,.08), transparent 30%),
            linear-gradient(135deg, rgba(19,34,52,.92), rgba(8,18,30,.96));
        box-shadow:
            0 25px 65px rgba(0,0,0,.30),
            inset 0 1px 0 rgba(255,255,255,.045);
    }

    .recommendation-priority {
        text-shadow: 0 0 22px rgba(230,185,74,.16);
    }

    /* Make the 3D visualization feel like a command viewport */
    [data-testid="stPlotlyChart"] {
        position: relative;
        background:
            radial-gradient(circle at 50% 50%, rgba(37,113,255,.05), transparent 55%),
            rgba(4,12,21,.35);
        box-shadow:
            0 30px 80px rgba(0,0,0,.34),
            inset 0 0 0 1px rgba(125,180,230,.05);
    }

    [data-testid="stPlotlyChart"]::after {
        content: "LIVE THERMAL FIELD";
        position: absolute;
        top: 14px;
        left: 18px;
        z-index: 2;
        padding: 5px 9px;
        border: 1px solid rgba(86,178,255,.13);
        border-radius: 999px;
        background: rgba(4,13,23,.62);
        color: rgba(148,205,245,.70);
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1.3px;
        pointer-events: none;
    }

    /* System health panel */
    .system-card {
        background:
            linear-gradient(180deg, rgba(14,29,46,.82), rgba(7,17,28,.88));
    }

    .system-row {
        transition: all .2s ease;
        padding-left: 8px;
        padding-right: 8px;
    }

    .system-row:hover {
        background: rgba(77,163,255,.035);
        transform: translateX(4px);
    }

    /* Premium button */
    div.stButton > button {
        min-height: 60px;
        border-radius: 17px;
        background:
            linear-gradient(110deg, #d8472f, #ef6843, #c83d2c);
        background-size: 200% 100%;
        box-shadow:
            0 14px 36px rgba(207,66,43,.24),
            inset 0 1px 0 rgba(255,255,255,.10);
        animation: buttonBreath 4s ease-in-out infinite;
    }

    div.stButton > button:hover {
        background-position: 100% 50%;
        box-shadow:
            0 18px 45px rgba(207,66,43,.34),
            0 0 30px rgba(255,103,67,.10);
    }

    /* Sidebar becomes a mission-control rail */
    [data-testid="stSidebar"] {
        box-shadow: 12px 0 50px rgba(0,0,0,.20);
    }

    [data-testid="stSidebar"]::before {
        content: "MISSION CONTROL";
        display: block;
        padding: 8px 0 14px;
        color: rgba(132,190,235,.45);
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 2px;
    }

    /* Analysis status container */
    [data-testid="stStatusWidget"] {
        border-radius: 18px !important;
        border: 1px solid rgba(88,175,240,.13) !important;
        background:
            linear-gradient(135deg, rgba(11,29,47,.90), rgba(7,17,28,.90)) !important;
        box-shadow:
            0 20px 50px rgba(0,0,0,.24),
            inset 0 1px 0 rgba(255,255,255,.04);
        animation: statusPanelIn .6s cubic-bezier(.2,.8,.2,1) both;
    }

    /* Page-level atmospheric scan */
    .block-container::after {
        content: "";
        position: fixed;
        left: 0;
        right: 0;
        top: -4px;
        height: 2px;
        z-index: 999;
        pointer-events: none;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(70,170,255,.35),
            rgba(255,103,67,.45),
            transparent
        );
        box-shadow: 0 0 18px rgba(80,170,255,.25);
        animation: pageScan 9s ease-in-out infinite;
    }

    @keyframes commandGrid {
        from { background-position: 0 0; }
        to { background-position: 44px 44px; }
    }

    @keyframes thermalAurora {
        from { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.08); }
        to { transform: rotate(360deg) scale(1); }
    }

    @keyframes heatText {
        from { background-position: 0% center; }
        to { background-position: 200% center; }
    }

    @keyframes commandOrb {
        from { transform: rotate(-18deg); }
        to { transform: rotate(342deg); }
    }

    @keyframes spectrumMove {
        from { background-position: 0% 50%; }
        to { background-position: 180% 50%; }
    }

    @keyframes buttonBreath {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.045); }
    }

    @keyframes statusPanelIn {
        from {
            opacity: 0;
            transform: translateY(10px) scale(.99);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes pageScan {
        0%, 35% {
            transform: translateY(0);
            opacity: 0;
        }
        45% {
            opacity: .8;
        }
        65%, 100% {
            transform: translateY(96vh);
            opacity: 0;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .stApp::before,
        .hero::before,
        .hero-title span,
        .hero-content::after,
        .metric-card::before,
        div.stButton > button,
        .block-container::after,
        [data-testid="stStatusWidget"] {
            animation: none !important;
        }
    }

    </style>
    """
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "result" not in st.session_state:
    st.session_state.result = None

if "activity_id" not in st.session_state:
    st.session_state.activity_id = None

if "recommendation" not in st.session_state:
    st.session_state.recommendation = None


# ============================================================
# HERO
# ============================================================

render_html(
    """
    <div class="hero">

        <div class="hero-content">

            <div class="hero-kicker">
                THERMAL INTELLIGENCE COMMAND CENTER
            </div>

            <div class="hero-title">
                THERMALYTIC <span>AI</span>
            </div>

            <div class="hero-subtitle">
                Heat-Aware Operations Intelligence
                <br>
                Real thermal intelligence for understanding
                temperature exposure, operational risk and
                safer planning.
            </div>

            <div class="hero-status">
                <span class="status-dot"></span>
                FORTYGUARD INTELLIGENCE READY
            </div>

        </div>

    </div>
    """
)


# ============================================================
# SIDEBAR
# ============================================================
st.session_state["_sidebar_enabled"] = True
with st.sidebar:

    st.markdown("## Analysis Settings")

    st.divider()

    st.markdown("### FortyGuard")

    st.caption(
        "Real thermal intelligence source"
    )

    st.markdown(
        "**Status:** :green[Connected]"
    )

    st.divider()

    st.markdown("### Thermal Analyzer")

    st.caption(
        "Risk and hotspot analysis engine"
    )

    st.markdown(
        "**Status:** :green[Active]"
    )

    st.divider()

    st.markdown("### Operations Recommender")

    st.caption(
        "Converts thermal risk into operational guidance"
    )

    st.markdown(
        "**Status:** :green[Active]"
    )

    st.divider()

    st.markdown("### Dataset")

    st.caption(
        "Thermal cells returned from FortyGuard"
    )

    st.markdown(
        "**Source:** :green[Real API]"
    )

    st.divider()

    st.markdown("### Platform")

    st.markdown(
        """
        Thermal intelligence  
        Risk analysis  
        Hotspot detection  
        Operational recommendations  
        3D visualization  
        Decision support
        """
    )


# ============================================================
# OPERATIONAL PLANNING INPUTS
# ============================================================

render_html(
    """
    <div class="section-title">
        Operational Planning
    </div>

    <div class="section-subtitle">
        Configure the operational conditions before
        requesting thermal intelligence from FortyGuard.
    </div>
    """
)

plan_col1, plan_col2, plan_col3 = st.columns(3)


with plan_col1:

    operation_type = st.selectbox(
        "Operation Type",
        [
            "Outdoor Construction",
            "Agricultural Work",
            "Road Maintenance",
            "Industrial Inspection",
            "Solar Field Maintenance",
            "Emergency Response",
            "General Outdoor Operations",
        ],
        index=0,
    )


with plan_col2:

    analysis_date = st.date_input(
        "Analysis Date",
        value=date(2024, 7, 15),
    )


with plan_col3:

    analysis_time = st.time_input(
        "Analysis Time",
        value=time(14, 0),
    )


# ============================================================
# OPERATIONAL AREA
# ============================================================

render_html(
    """
    <div class="section-title">
        Operational Area
    </div>

    <div class="section-subtitle">
        Define the center point and size of the operational
        area to be analyzed.
    </div>
    """
)


area_col1, area_col2 = st.columns(2)


with area_col1:

    latitude = st.number_input(
        "Center Latitude",
        value=33.4450,
        format="%.4f",
    )


with area_col2:

    longitude = st.number_input(
        "Center Longitude",
        value=-112.0750,
        format="%.4f",
    )


# ============================================================
# OPERATIONAL AREA SIZE
# ============================================================

size_col1, size_col2 = st.columns(2)


with size_col1:

    area_width = st.number_input(
        "Area Width (degrees)",
        min_value=0.0010,
        max_value=1.0000,
        value=0.0100,
        step=0.0010,
        format="%.4f",
    )


with size_col2:

    area_height = st.number_input(
        "Area Height (degrees)",
        min_value=0.0010,
        max_value=1.0000,
        value=0.0100,
        step=0.0010,
        format="%.4f",
    )


# ============================================================
# CALCULATE OPERATIONAL BOUNDARY
# ============================================================

half_width = area_width / 2
half_height = area_height / 2

min_longitude = longitude - half_width
max_longitude = longitude + half_width

min_latitude = latitude - half_height
max_latitude = latitude + half_height


# ============================================================
# FORTYGUARD PAYLOAD
# ============================================================

half_width = area_width / 2.0
half_height = area_height / 2.0

west = longitude - half_width
east = longitude + half_width
south = latitude - half_height
north = latitude + half_height

payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "operation_type": operation_type,
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [west, south],
                        [east, south],
                        [east, north],
                        [west, north],
                        [west, south],
                    ]],
                },
            }
        ],
    },
    "date_time": {
        "start_date": analysis_date.strftime("%Y-%m-%d"),
        "start_time": analysis_time.strftime("%H:%M"),
        "filter_type": 1,
    },
    "granularity": 100,
    "analytic_type": "tcm",
}

# ============================================================
# ANALYSIS HEADER
# ============================================================
# ANALYSIS HEADER
# ============================================================

render_html(
    """
    <div class="section-title">
        Thermal Analysis
    </div>

    <div class="section-subtitle">
        Submit the operational area to FortyGuard and
        generate real thermal intelligence.
    </div>
    """
)


# ============================================================
# RUN BUTTON
# ============================================================

run_analysis = st.button(
    "Run Real FortyGuard Analysis",
    type="primary",
)


# ============================================================
# RUN ANALYSIS
# ============================================================

if run_analysis:

    try:

        with st.status(
            "Connecting to FortyGuard...",
            expanded=True
        ) as status:

            # ------------------------------------------------
            # STEP 1 — FORTYGUARD
            # ------------------------------------------------

            st.write(
                "Submitting thermal analysis..."
            )

            if not (-90 <= latitude <= 90):
                raise ValueError(
                    "Center latitude must be between -90 and 90."
                )

            if not (-180 <= longitude <= 180):
                raise ValueError(
                    "Center longitude must be between -180 and 180."
                )

            if area_width <= 0 or area_height <= 0:
                raise ValueError(
                    "Area width and height must be greater than zero."
                )

            client = FortyGuardClient()

            submission = client.create_heatmap(
                payload
            )

            activity_id = (
                submission
                .get("data", {})
                .get("activity_id")
            )

            if not activity_id:

                raise RuntimeError(
                    "FortyGuard did not return an activity ID."
                )

            st.session_state.activity_id = activity_id

            st.write(
                f"Activity ID: `{activity_id}`"
            )

            st.write(
                "Waiting for FortyGuard thermal processing..."
            )

            result = client.wait_for_completion(
                activity_id
            )

            st.session_state.result = result

            st.write(
                "FortyGuard processing completed."
            )

            # ------------------------------------------------
            # STEP 2 — THERMAL ANALYZER
            # ------------------------------------------------

            st.write(
                "Running ThermalAnalyzer..."
            )

            analyzer = ThermalAnalyzer()

            analysis = analyzer.analyze(
                result
            )

            st.session_state.analysis = analysis

            total_cells = int(analysis.get("total_cells", 0))

            if total_cells == 0:
                st.warning(
                    "No thermal observations are available for the "
                    "selected operational area and analysis time. "
                    "FortyGuard completed the request successfully, "
                    "but returned zero thermal cells. Please choose "
                    "another supported date/time or operational area."
                )
                st.info(
                    "The FortyGuard connection is working. No synthetic "
                    "or fallback temperature data will be displayed."
                )
                st.session_state.analysis = None
                st.session_state.recommendation = None
                st.session_state.thermal_df = None
                st.stop()


            st.write(
                "Thermal risk analysis completed."
            )

            # ------------------------------------------------
            # STEP 3 — OPERATIONS RECOMMENDER
            # ------------------------------------------------

            st.write(
                "Generating operational recommendation..."
            )

            

            recommender = OperationsRecommender()
  
                 

            recommendation = recommender.recommend(
                 analysis,
                 operation_type,
            )

            st.session_state.recommendation = recommendation
                
                
        
    
        
            st.write(
                "Operational recommendation generated."
            )

            # ------------------------------------------------
            # COMPLETE
            # ------------------------------------------------

            status.update(
                label="Thermal analysis completed",
                state="complete",
                expanded=False,
            )

    except Exception as error:

        st.error(
            f"Analysis failed: {error}"
        )

        st.stop()


# ============================================================
# GET ANALYSIS
# ============================================================

analysis = st.session_state.analysis


# ============================================================
# EMPTY STATE
# ============================================================

if analysis is None:

    render_html(
        """
        <div class="risk-card">

            <div class="risk-title">
                Ready for Thermal Intelligence
            </div>

            <div class="risk-description">
                Run the analysis to retrieve real
                FortyGuard thermal data and generate
                the complete THERMALYTIC AI dashboard.
            </div>

        </div>
        """
    )

    render_html(
        """
        <div class="footer">
            <b>THERMALYTIC AI</b>
            — Heat-Aware Operations Intelligence
        </div>
        """
    )

    st.stop()


# ============================================================
# EXTRACT DATA
# ============================================================

total_cells = int(
    analysis.get(
        "total_cells",
        0
    )
)

statistics = analysis.get(
    "statistics",
    {}
)

minimum = float(
    statistics.get(
        "minimum",
        0
    )
)

maximum = float(
    statistics.get(
        "maximum",
        0
    )
)

mean = float(
    statistics.get(
        "mean",
        0
    )
)

temperature_range = float(
    statistics.get(
        "range",
        maximum - minimum
    )
)

overall_risk = str(
    analysis.get(
        "overall_risk",
        "UNKNOWN"
    )
)

hotspot_count = int(
    analysis.get(
        "hotspot_count",
        0
    )
)

hotspots = analysis.get(
    "hotspots",
    []
)

cells = analysis.get(
    "cells",
    []
)


# ============================================================
# SUCCESS
# ============================================================

st.success(
    "Real FortyGuard thermal intelligence received successfully."
)

if st.session_state.activity_id:

    st.caption(
        f"Activity ID: {st.session_state.activity_id}"
    )


# ============================================================
# THERMAL OVERVIEW
# ============================================================

render_html(
    """
    <div class="section-title">
        Thermal Intelligence Overview
    </div>
    """
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Thermal Cells
            </div>

            <div class="metric-value">
                {total_cells}
            </div>

            <div class="metric-small">
                Real FortyGuard cells
            </div>

        </div>
        """
    )


with col2:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Minimum
            </div>

            <div class="metric-value">
                {minimum:.2f} °C
            </div>

            <div class="metric-small">
                Lowest recorded temperature
            </div>

        </div>
        """
    )


with col3:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Maximum
            </div>

            <div class="metric-value">
                {maximum:.2f} °C
            </div>

            <div class="metric-small">
                Highest recorded temperature
            </div>

        </div>
        """
    )


with col4:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Mean
            </div>

            <div class="metric-value">
                {mean:.2f} °C
            </div>

            <div class="metric-small">
                Average thermal exposure
            </div>

        </div>
        """
    )


# ============================================================
# RISK ASSESSMENT
# ============================================================

render_html(
    """
    <div class="section-title">
        Risk Assessment
    </div>
    """
)


risk_upper = overall_risk.upper()


if risk_upper == "HIGH":

    risk_icon = "HIGH"

elif risk_upper == "LOW":

    risk_icon = "LOW"

else:

    risk_icon = "MODERATE"


render_html(
    f"""
    <div class="risk-card">

        <div class="risk-title">
            {risk_icon} RISK
        </div>

        <div class="risk-description">
            Thermal exposure should be considered when
            planning operations. THERMALYTIC AI uses
            returned thermal intelligence to identify
            temperature exposure and potential
            operational risk.
        </div>

    </div>
    """
)


# ============================================================
# EXPLAINABLE DECISION INTELLIGENCE
# ============================================================

render_html(
    """
    <div class="section-title">
        Decision Intelligence
    </div>

    <div class="section-subtitle">
        Explainable factors behind the current thermal
        operational decision.
    </div>
    """
)

# ------------------------------------------------------------
# Determine primary risk factor
# ------------------------------------------------------------

if overall_risk.upper() == "HIGH":

    primary_factor = (
        "High overall thermal exposure"
    )

elif mean >= 40:

    primary_factor = (
        "Elevated mean temperature"
    )

elif hotspot_count > 0:

    primary_factor = (
        "Thermal hotspots detected"
    )

elif overall_risk.upper() == "MODERATE":

    primary_factor = (
        "Moderate overall thermal exposure"
    )

else:

    primary_factor = (
        "Low overall thermal exposure"
    )


# ------------------------------------------------------------
# Determine secondary factor
# ------------------------------------------------------------

if hotspot_count > 0:

    secondary_factor = (
        f"{hotspot_count} thermal hotspot cell(s) "
        "require attention"
    )

elif temperature_range >= 10:

    secondary_factor = (
        "Large temperature variation exists "
        "across the analyzed area"
    )

else:

    secondary_factor = (
        "No significant hotspot concentration detected"
    )


# ------------------------------------------------------------
# Operational impact
# ------------------------------------------------------------

if overall_risk.upper() == "HIGH":

    operational_impact = (
        "Higher thermal exposure may increase operational "
        "stress during outdoor activities."
    )

elif overall_risk.upper() == "MODERATE":

    operational_impact = (
        "Thermal exposure should be considered when "
        "planning outdoor operations."
    )

else:

    operational_impact = (
        "Current thermal conditions are generally suitable "
        "for normal operations."
    )


# ------------------------------------------------------------
# Render explanation
# ------------------------------------------------------------

render_html(
    f"""
    <div class="recommendation-card">

        <div class="recommendation-header">

            <div>
                <div class="recommendation-label">
                    PRIMARY RISK FACTOR
                </div>

                <div class="recommendation-priority">
                    {primary_factor}
                </div>
            </div>

        </div>


        <div class="recommendation-grid">

            <div class="recommendation-item">

                <div class="recommendation-item-label">
                    Mean Temperature
                </div>

                <div class="recommendation-item-text">
                    {mean:.2f} °C
                </div>

            </div>


            <div class="recommendation-item">

                <div class="recommendation-item-label">
                    Maximum Temperature
                </div>

                <div class="recommendation-item-text">
                    {maximum:.2f} °C
                </div>

            </div>


            <div class="recommendation-item">

                <div class="recommendation-item-label">
                    Thermal Hotspots
                </div>

                <div class="recommendation-item-text">
                    {hotspot_count}
                </div>

            </div>


            <div class="recommendation-item">

                <div class="recommendation-item-label">
                    Temperature Range
                </div>

                <div class="recommendation-item-text">
                    {temperature_range:.2f} °C
                </div>

            </div>


            <div class="recommendation-item">

                <div class="recommendation-item-label">
                    Secondary Factor
                </div>

                <div class="recommendation-item-text">
                    {secondary_factor}
                </div>

            </div>


            <div class="recommendation-item">

                <div class="recommendation-item-label">
                    Operational Impact
                </div>

                <div class="recommendation-item-text">
                    {operational_impact}
                </div>

            </div>

        </div>

    </div>
    """
)

recommendation = st.session_state.recommendation

if recommendation:

    priority = str(
        recommendation.get(
            "priority",
            "UNKNOWN"
        )
    ).upper()

    recommendation_text = recommendation.get(
        "recommendation",
        "No recommendation available."
    )

    reason = recommendation.get(
        "reason",
        "No reason available."
    )

    action = recommendation.get(
        "action",
        "Review thermal conditions before proceeding."
    )

    render_html(
        """
        <div class="section-title">
            Operational Recommendation
        </div>

        <div class="section-subtitle">
            Decision support generated from the thermal
            analysis and operational risk assessment.
        </div>
        """
    )

    render_html(
        f"""
        <div class="recommendation-card">

            <div class="recommendation-header">

                <div>

                    <div class="recommendation-label">
                        OPERATIONAL PRIORITY
                    </div>

                    <div class="recommendation-priority">
                        {priority}
                    </div>

                </div>

            </div>

            <div class="recommendation-main">
                {recommendation_text}
            </div>

            <div class="recommendation-grid">

                <div class="recommendation-item">

                    <div class="recommendation-item-label">
                        Reason
                    </div>

                    <div class="recommendation-item-text">
                        {reason}
                    </div>

                </div>

                <div class="recommendation-item">

                    <div class="recommendation-item-label">
                        Recommended Action
                    </div>

                    <div class="recommendation-item-text">
                        {action}
                    </div>

                </div>

            </div>

        </div>
        """
    )


# ============================================================
# TEMPERATURE EXPOSURE
# ============================================================

render_html(
    """
    <div class="section-title">
        Temperature Exposure
    </div>
    """
)


col1, col2, col3 = st.columns(3)


with col1:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Temperature Difference
            </div>

            <div class="metric-value">
                {temperature_range:.2f} °C
            </div>

            <div class="metric-small">
                Maximum minus minimum
            </div>

        </div>
        """
    )


with col2:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Hotspot Cells
            </div>

            <div class="metric-value">
                {hotspot_count}
            </div>

            <div class="metric-small">
                Detected by ThermalAnalyzer
            </div>

        </div>
        """
    )


with col3:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Standardized Risk
            </div>

            <div class="metric-value">
                {risk_upper}
            </div>

            <div class="metric-small">
                ThermalAnalyzer assessment
            </div>

        </div>
        """
    )


# ============================================================
# HOTSPOTS
# ============================================================

render_html(
    """
    <div class="section-title">
        Top Thermal Hotspots
    </div>
    """
)


sorted_hotspots = sorted(
    hotspots,
    key=lambda item: float(
        item.get(
            "temperature_c",
            0
        )
    ),
    reverse=True,
)


if not sorted_hotspots:

    st.info(
        "No hotspot cells were detected by the "
        "current ThermalAnalyzer thresholds."
    )

else:

    for cell in sorted_hotspots[:10]:

        temperature = float(
            cell.get(
                "temperature_c",
                0
            )
        )

        score = float(
            cell.get(
                "risk_score",
                0
            )
        )

        tile_id = cell.get(
            "tile_id",
            "Unknown"
        )

        risk_level = cell.get(
            "risk_level",
            "UNKNOWN"
        )

        render_html(
            f"""
            <div class="hotspot-card">

                <b>Tile {tile_id}</b>

                &nbsp;&nbsp;

                {temperature:.2f} °C

                &nbsp;&nbsp; | &nbsp;&nbsp;

                Risk: {risk_level}

                &nbsp;&nbsp; | &nbsp;&nbsp;

                Score: {score:.2f}

            </div>
            """
        )


# ============================================================
# 3D THERMAL ENVIRONMENT
# ============================================================

render_html(
    """
    <div class="section-title">
        3D Thermal Environment
    </div>

    <div class="section-subtitle">
        Interactive visualization built from real
        FortyGuard thermal cells. Drag to rotate,
        scroll to zoom and hover over cells for
        temperature information.
    </div>
    """
)


# ============================================================
# RAW FORTYGUARD DATA
# ============================================================

result = st.session_state.result or {}

result_data = (
    result
    .get("data", {})
    .get("result", {})
)

map_data = result_data.get(
    "map_data",
    {}
)

features = map_data.get(
    "features",
    []
)


# ============================================================
# BUILD 3D MODEL
# ============================================================

x_values = []
y_values = []
z_values = []

i_values = []
j_values = []
k_values = []

temperatures = []

vertex_index = 0

temperature_span = max(
    maximum - minimum,
    0.001
)


for feature in features:

    geometry = feature.get(
        "geometry",
        {}
    )

    properties = feature.get(
        "properties",
        {}
    )

    coordinates = geometry.get(
        "coordinates",
        []
    )

    if not coordinates:
        continue

    polygon = coordinates[0]

    if len(polygon) < 4:
        continue

    temperature = properties.get(
        "average_temperature",
        mean
    )

    try:

        temperature = float(
            temperature
        )

    except (TypeError, ValueError):

        temperature = mean

    corners = polygon[:4]

    for lon, lat in corners:

        x_values.append(
            float(lon)
        )

        y_values.append(
            float(lat)
        )

        normalized = (
            temperature - minimum
        ) / temperature_span

        # Visual exaggeration only.
        # Real temperature remains unchanged
        # in the color scale.

        z_values.append(
            normalized * 12.0
        )

        temperatures.append(
            temperature
        )

    i_values.extend(
        [
            vertex_index,
            vertex_index
        ]
    )

    j_values.extend(
        [
            vertex_index + 1,
            vertex_index + 2
        ]
    )

    k_values.extend(
        [
            vertex_index + 2,
            vertex_index + 3
        ]
    )

    vertex_index += 4


# ============================================================
# CREATE 3D PLOT
# ============================================================

if x_values:

    fig = go.Figure()

    fig.add_trace(
        go.Mesh3d(

            x=x_values,
            y=y_values,
            z=z_values,

            i=i_values,
            j=j_values,
            k=k_values,

            intensity=temperatures,

            intensitymode="vertex",

            colorscale=[
                [0.00, "#253BFF"],
                [0.20, "#16A7E8"],
                [0.40, "#20D39A"],
                [0.60, "#D9E63F"],
                [0.78, "#FF9A3D"],
                [0.90, "#F14C45"],
                [1.00, "#D946EF"],
            ],

            cmin=minimum,
            cmax=maximum,

            showscale=True,

            colorbar=dict(

                title=dict(
                    text="Temperature °C",
                    font=dict(
                        color="#d9e2ef",
                        size=13,
                    ),
                ),

                tickfont=dict(
                    color="#b6c3d4",
                    size=11,
                ),

                thickness=16,

                len=0.70,
            ),

            flatshading=False,

            lighting=dict(
                ambient=0.50,
                diffuse=0.80,
                specular=0.55,
                roughness=0.40,
                fresnel=0.20,
            ),

            lightposition=dict(
                x=100,
                y=200,
                z=300,
            ),

            hovertemplate=(
                "<b>Thermal Cell</b><br>"
                "Temperature: %{intensity:.2f} °C"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(

        height=650,

        margin=dict(
            l=0,
            r=0,
            t=10,
            b=0,
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        scene=dict(

            bgcolor="rgba(0,0,0,0)",

            xaxis=dict(
                title="Longitude",
                color="#8290a5",
                gridcolor="rgba(150,190,230,0.08)",
                zerolinecolor="rgba(150,190,230,0.08)",
            ),

            yaxis=dict(
                title="Latitude",
                color="#8290a5",
                gridcolor="rgba(150,190,230,0.08)",
                zerolinecolor="rgba(150,190,230,0.08)",
            ),

            zaxis=dict(
                title="Thermal Intensity",
                color="#8290a5",
                gridcolor="rgba(150,190,230,0.08)",
                zerolinecolor="rgba(150,190,230,0.08)",
            ),

            aspectmode="auto",

            camera=dict(
                eye=dict(
                    x=1.65,
                    y=1.65,
                    z=1.20,
                )
            ),
        ),

        showlegend=False,
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": True,
            "scrollZoom": True,
            "displaylogo": False,
            "responsive": True,
        },
    )

else:

    st.warning(
        "No thermal geometry was available "
        "for 3D visualization."
    )


# ============================================================
# SAMPLE THERMAL CELL
# ============================================================

render_html(
    """
    <div class="section-title">
        Sample Thermal Cell
    </div>
    """
)


if cells:

    first_cell = cells[0]

    tile_id = first_cell.get(
        "tile_id",
        0
    )

    cell_temperature = float(
        first_cell.get(
            "temperature_c",
            mean
        )
    )

    cell_risk = first_cell.get(
        "risk_level",
        "UNKNOWN"
    )

    cell_score = float(
        first_cell.get(
            "risk_score",
            0
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Tile ID
                </div>

                <div class="metric-value">
                    {tile_id}
                </div>

                <div class="metric-small">
                    Thermal grid cell
                </div>

            </div>
            """
        )

    with col2:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Temperature
                </div>

                <div class="metric-value">
                    {cell_temperature:.2f} °C
                </div>

                <div class="metric-small">
                    Recorded temperature
                </div>

            </div>
            """
        )

    with col3:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Risk Level
                </div>

                <div class="metric-value">
                    {cell_risk}
                </div>

                <div class="metric-small">
                    ThermalAnalyzer
                </div>

            </div>
            """
        )

    with col4:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Risk Score
                </div>

                <div class="metric-value">
                    {cell_score:.2f}
                </div>

                <div class="metric-small">
                    Standardized score
                </div>

            </div>
            """
        )


# ============================================================
# SYSTEM STATUS
# ============================================================

render_html(
    """
    <div class="section-title">
        System Status
    </div>
    """
)


render_html(
    """
    <div class="system-card">

        <div class="system-row">

            <span class="system-name">
                FortyGuard API
            </span>

            <span class="system-status">
                CONNECTED
            </span>

        </div>

        <div class="system-row">

            <span class="system-name">
                Thermal Analyzer
            </span>

            <span class="system-status">
                ACTIVE
            </span>

        </div>

        <div class="system-row">

            <span class="system-name">
                Operations Recommender
            </span>

            <span class="system-status">
                ACTIVE
            </span>

        </div>

        <div class="system-row">

            <span class="system-name">
                Thermal Dataset
            </span>

            <span class="system-status">
                LOADED
            </span>

        </div>

        <div class="system-row">

            <span class="system-name">
                3D Thermal Engine
            </span>

            <span class="system-status">
                ACTIVE
            </span>

        </div>

    </div>
    """
)


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        <b>THERMALYTIC AI</b>
        — Heat-Aware Operations Intelligence

        <br>

        Powered by real FortyGuard thermal intelligence

    </div>
    """
)