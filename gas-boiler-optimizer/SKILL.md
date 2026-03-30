---
name: gas-boiler-optimizer
description: Optimize old atmospheric gas boiler (Junkers Euroline E6 or similar) for minimum gas consumption. Covers built-in hysteresis behavior, room thermostat priority, night setback, and supply temperature tuning for cold climates.
---

# Gas Boiler Optimizer — Junkers Euroline E6

Expert advisor for reducing gas consumption on old atmospheric gas boilers with E6-type controllers and room temperature sensors, while maintaining comfort. Validated for cold climates (Latvia, Baltic, Nordic).

## When to Use

- High gas bill, want to find where gas is wasted
- Boiler cycles too often or too rarely
- Deciding correct supply water temperature setpoint
- Evaluating night setback vs. full overnight shutdown
- Understanding what the room thermostat actually controls vs. what the boiler aquastat controls

## When NOT to Use

- Condensing boilers (return temperature constraints are different)
- Underfloor heating (low-temperature logic needed)
- Emergency faults, gas leaks, or error codes — call a technician

---

## Critical: How Junkers E6 Hysteresis Works

**This is the most important thing to understand before changing any settings.**

The E6 controller has a **fixed built-in asymmetric hysteresis** — it cannot be changed by the user:

| Setpoint | Burner OFF at | Burner ON at | Total swing |
|---|---|---|---|
| 75°C | 85°C (+10°C) | 55°C (-20°C) | 30°C |
| 65°C | 75°C (+10°C) | 45°C (-20°C) | 30°C |
| 55°C | 65°C (+10°C) | 35°C (-20°C) | 30°C |

**What this means in practice:**
- The boiler always overshoots setpoint by 10°C before stopping
- The boiler waits until water cools 20°C below setpoint before restarting
- This wide swing is intentional — it prevents short cycling at the boiler level
- You **cannot** narrow or widen this hysteresis — it is hardwired in E6

**Consequence:** If you set the boiler to 75°C, it actually delivers water between 55°C and 85°C. Plan your comfort around the average (~70°C), not the setpoint.

---

## Control Hierarchy: What Controls What

```
Room thermostat (TA terminals)
    ↓ calls for heat ON/OFF
Boiler aquastat (E6 controller)
    ↓ maintains water temp within its fixed hysteresis
Burner
```

**Room thermostat = master switch.** When room reaches target → thermostat opens circuit → boiler stops firing completely regardless of water temperature.

**Boiler aquastat = temperature keeper.** Only active when room thermostat is calling for heat.

**Common mistake:** Bypassing room thermostat (TA terminals jumpered) and controlling everything via water setpoint — this removes room-level feedback and wastes gas because boiler fires based on water temperature, not actual room need.

---

## Step 1: Verify Room Thermostat Is Wired Correctly

Check terminals marked **TA** on the E6 controller board:
- **Correct:** Room thermostat connected, jumper removed → thermostat controls when boiler fires
- **Wrong:** Jumper still in place, thermostat ignored → boiler fires by water temp only

If thermostat is correctly connected: **estimated gas saving 15–20%** vs. jumpered mode (confirmed by multiple sources including Russian heating forums and Junkers documentation).

---

## Step 2: Set the Right Water Temperature Setpoint

With E6's fixed hysteresis, the setpoint determines the average operating range. Choose based on outdoor temperature:

**For old uninsulated / Soviet-era panel building:**

| Outdoor temp | Recommended setpoint | Actual water range |
|---|---|---|
| -15°C and below | 75–80°C | 55–90°C |
| -5°C to -15°C | 70°C | 50–80°C |
| 0°C to -5°C | 65°C | 45–75°C |
| +5°C | 55–60°C | 35–70°C |
| +10°C | 50°C | 30–60°C |
| above +14°C | turn off | — |

**For renovated / insulated building:**
Subtract 10–15°C from each setpoint above.

**Rule:** Every 10°C reduction in average supply temperature → ~3–5% gas saving from reduced standing losses and pipe radiation. Lower setpoint also means longer burn cycles (good).

---

## Step 3: Night Setback Strategy for Latvia

Latvia design temperature: -18°C to -20°C. Heating season: October–April.

**Do NOT fully shut down overnight when outdoor temp is below -5°C.**

Reason: Old buildings with high heat loss require 3–5 hours to reheat from cold. The reheat burst consumes more gas than maintaining a lower temperature overnight.

| Outdoor temp | Recommended night strategy |
|---|---|
| Below -10°C | Keep room thermostat at 17–18°C (setback only 3–4°C) |
| -5°C to -10°C | Setback to 16–17°C |
| 0°C to -5°C | Setback to 15–16°C, or full shutdown acceptable |
| Above 0°C | Full overnight shutdown acceptable |
| Weekend / 2+ days away | Lower to 14–15°C frost protection, never fully off in winter |

**How to implement with E6 + room thermostat:**
- Use a programmable thermostat (e.g. Auraton, IMIT, Salus) connected to TA terminals
- Set day program: 21°C, night program: 17°C
- The boiler aquastat and setpoint do not change — only the room thermostat schedule changes

**Expected saving from night setback:** 8–12% of seasonal gas consumption.

---

## Step 4: Diagnose Cycling Problems

With E6's wide 30°C hysteresis, the boiler itself rarely short-cycles. If you still see frequent cycling, the cause is almost always the **room thermostat**, not the boiler.

**Diagnosing room thermostat cycling:**

| Symptom | Cause | Fix |
|---|---|---|
| Boiler fires for 2–3 min then stops | Room thermostat too close to heat source (boiler, radiator, sunny window) | Relocate thermostat to inner wall, away from heat sources |
| Room temp swings ±3–4°C | Thermostat hysteresis too narrow or bimetallic type | Replace with electronic thermostat (hysteresis 0.3–0.5°C) |
| Boiler runs but room stays cold | Thermostat correctly signals but boiler setpoint too low for heat loss | Raise setpoint 5°C, wait 30 min, check radiator temperature |
| Boiler never stops | Room thermostat stuck closed or jumper left in | Check TA terminals |

**Good cycling rhythm with E6 + room thermostat:**
- Burner on: 15–30 minutes (boiler fills thermal mass of radiators)
- Burner off: 20–60 minutes (room coasts on stored heat)
- Daily cycles: 8–15 in cold weather, 4–8 in mild weather

---

## Step 5: Dry Cycling — Hidden Gas Waste

**Dry cycling** = boiler fires to maintain its own water temperature when no room heat is needed (room thermostat satisfied, but boiler cools and refires just to keep water hot).

**Impact:** Up to 10–25% of gas consumption wasted on dry cycling (source: Sabien Technology, DOE studies).

**With E6 + room thermostat correctly wired:** Dry cycling is minimized because room thermostat cuts power to burner when room is satisfied.

**If room thermostat is bypassed (jumpered TA):** Boiler dry-cycles constantly — fires to 85°C, cools to 55°C, fires again, all day, even when rooms are warm. This is the single biggest source of gas waste on this type of boiler.

---

## Step 6: Optimal Setpoint — Standing Losses vs. Cycling Losses

This is the most common question: should you heat water to 80°C so the boiler fires rarely, or keep it at 60°C accepting more frequent cycles?

**Real measured experiment** (Viessmann 24kW, wooden house 38m², outdoor -8°C):

| Setpoint | Gas cost | Pump electricity | Total cost |
|---|---|---|---|
| 40°C | high | very high (pump never stops) | most expensive |
| 50°C | medium | high | expensive |
| **60°C** | **medium** | **low** | **optimal** |
| 70°C | slightly higher | minimal | slightly worse than 60°C |

**Why 40°C is worse despite low setpoint:** pump runs almost continuously, adding 3.5× electricity cost. Water never gets hot enough, radiators underperform, thermostat never satisfies.

**Why 80°C is worse despite fewer cycles:** standing losses from a hot boiler in a cold basement are proportional to temperature difference. At 80°C in a 15°C basement (65°C delta) vs. 60°C (45°C delta) — losses are ~44% higher during every idle period.

**For Junkers E6 specifically:** setpoint 65°C gives actual water range 45–75°C (average ~60°C). This is the optimum for Latvia winter conditions.

**Hard limits for atmospheric boiler:**
- **Minimum 55°C setpoint** — below this, return water can drop under 45°C causing condensation in flue and corrosion of heat exchanger
- **Maximum 80°C** — above this, standing losses grow rapidly, polypropylene pipes degrade faster

---

## Step 7: Flue Draft Loss During Standby (Open Chimney)

Atmospheric boilers like Junkers E6 have an **open flue** — no automatic damper. When the burner is off, warm air from the boiler room rises through the chimney by natural convection and escapes outside.

**Measured impact:** DOE estimates a **vent damper saves 5–10% of annual gas consumption** on atmospheric boilers. This is the loss you have without one.

**How significant is it?**
- Active loss (gases during combustion): 14–19% of gas energy goes up the flue — unavoidable
- Standby loss (convection when burner off): smaller but continuous — depends on chimney height, diameter, and temperature difference

**What you can do without a damper:**
- Keep boiler room door closed — reduces convection driving force
- Ensure chimney is not oversized for the boiler — excess diameter increases draft loss
- Lower setpoint reduces temperature of boiler body → less convection in standby

**Hardware fix:** Install a flue damper (electromechanical, closes when burner shuts off). Payback: 1–2 heating seasons. This is a separate upgrade from the boiler itself.

---

## Practical Optimization Checklist

Before adjusting anything — measure for 3 days:
- [ ] Note current gas meter reading each morning
- [ ] Count how many times burner fires per hour (listen for click + flame sound)
- [ ] Check if room thermostat TA terminals have jumper or thermostat connected

Then apply in order (one change at a time, 3 days between):

1. **Connect room thermostat to TA** if not done — biggest single gain (15–20%)
2. **Lower boiler setpoint** to 65°C for typical Latvia winter — optimal balance (3–5%)
3. **Set night setback** on programmable thermostat (8–12% additional)
4. **Relocate thermostat** if it's near heat source (stops phantom cycling)
5. **Balance radiators** — close lockshield valves on overheated rooms, open on cold rooms
6. **Install flue damper** on chimney — blocks standby draft loss (5–10%)

**Realistic total saving potential for Junkers E6 with all steps:** 25–40% vs. unoptimized state.

---

## What Cannot Be Changed on E6

| Parameter | Changeable? | Notes |
|---|---|---|
| Aquastat hysteresis (30°C swing) | No | Hardwired in E6 |
| Burner modulation | No | E6 is on/off only |
| Weather compensation | No | E6 has no outdoor sensor input |
| DHW priority | Yes | Via front panel selector |
| Supply temperature setpoint | Yes | Main rotary knob |

To get weather compensation or modulation on this boiler, you need an **external weather-compensating controller** wired to TA terminals — the E6 then becomes a slave that fires on demand. This is a hardware upgrade, not a settings change.

---

## Sources and Validation

Key data points validated from:
- Junkers Euroline ZW 18/23-1 KE/AE official manual (hysteresis values: +10°C/-20°C)
- Sabien Technology boiler cycling research (10–25% dry cycling waste)
- Mastergrad.ru heating forum (room thermostat saves ~20%, cycling diagnosis)
- EEVBlog heating engineering forum (buffer tank, cycling optimization)
- Energy Vanguard research (night setback effectiveness in cold climates)
- DOE / NREL Minimizing Boiler Short Cycling Losses (efficiency drop from cycling)
- tol.acritum.com real measured experiment (optimal setpoint 60°C confirmed)
- Heating Help: The Wall forum (standby losses ~20,000 BTU/hr measured)
- DOE Energy Saver (vent damper saves 5–10% annually on atmospheric boilers)
