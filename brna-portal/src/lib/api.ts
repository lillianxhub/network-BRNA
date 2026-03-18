import { mockTestScenarios, generateMockStatusData, generateMockTestStatus } from '../mock/data';

const API_BASE = "http://localhost:8000";
export const IS_DEMO = process.env.NEXT_PUBLIC_DEMO === "true";

// Mutable mock state for demo mode
let simProgress = 0;
let isSimRunning = false;
let testProgress = 0;
let activeTestId: string | null = null;
let isTestRunning = false;

if (IS_DEMO && typeof window !== 'undefined') {
  // Simulate progress when running
  setInterval(() => {
    if (isSimRunning) {
      simProgress += 5;
      if (simProgress >= 100) {
        simProgress = 100;
        isSimRunning = false;
      }
    }
    if (isTestRunning) {
      testProgress += 10;
      if (testProgress >= 100) {
        testProgress = 100;
        isTestRunning = false;
      }
    }
  }, 1000);
}

export async function fetchTestScenarios() {
  if (IS_DEMO) {
    // Artificial small delay
    await new Promise(r => setTimeout(r, 200));
    return mockTestScenarios;
  }
  const res = await fetch(`${API_BASE}/test-scenarios`);
  return res.json();
}

export async function fetchStatus() {
  if (IS_DEMO) {
    return generateMockStatusData(isSimRunning, simProgress);
  }
  const res = await fetch(`${API_BASE}/status`);
  return res.json();
}

export async function fetchTestStatus() {
  if (IS_DEMO) {
    return generateMockTestStatus(isTestRunning, activeTestId, testProgress);
  }
  const res = await fetch(`${API_BASE}/test-status`);
  return res.json();
}

export async function startSimulation() {
  if (IS_DEMO) {
    isSimRunning = true;
    simProgress = 0;
    return { status: "started" };
  }
  const res = await fetch(`${API_BASE}/simulate`, { method: "POST" });
  // if endpoint doesn't return JSON, this might fail, but original page.tsx didn't await JSON, just POSTed.
  // wait, page.tsx just did `await fetch` and didn't read json. I'll just return OK.
  return { status: res.ok ? "started" : "error" };
}

export async function runTestScenario(id: string) {
  if (IS_DEMO) {
    activeTestId = id;
    isTestRunning = true;
    testProgress = 0;
    return { status: "started" };
  }
  const res = await fetch(`${API_BASE}/run-test/${id}`, { method: "POST" });
  return { status: res.ok ? "started" : "error" };
}
