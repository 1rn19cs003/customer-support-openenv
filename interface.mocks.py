"""
Mock Test Interface for Customer Support Environment
Tests all 3 tasks with structured output validation
No external APIs required - runs completely locally
"""

import sys
import random
from server.environment import MyEnvironment
from pydantic import BaseModel

# Force flush stdout for proper output
sys.stdout.reconfigure(line_buffering=True)

class Action(BaseModel):
    action_type: str
    content: str | None = None

class MockAgent:
    """Simple rule-based agent for testing"""
    
    def __init__(self):
        self.env = MyEnvironment()
    
    def get_action(self, difficulty, step, previous_actions=None):
        """
        Returns action based on difficulty and step
        Simulates different agent behaviors
        """
        if difficulty == "easy":
            # Easy task: always correct category
            return {
                "action_type": "technical",
                "content": "Please reset your password. Go to login page and click 'Forgot Password'."
            }
        
        elif difficulty == "medium":
            # Medium task: sometimes makes mistakes
            if step == 1:
                # First step might be wrong category
                if random.random() < 0.3:  # 30% chance of wrong category
                    return {
                        "action_type": "technical",  # Wrong! Should be billing
                        "content": "I'll help you with your account issue."
                    }
                else:
                    return {
                        "action_type": "billing",
                        "content": "We are checking your refund status. Please allow 5-7 business days."
                    }
            else:
                # Subsequent steps correct
                return {
                    "action_type": "billing",
                    "content": "Your refund is being processed. We'll notify you via email."
                }
        
        else:  # hard
            # Hard task: complex decision making
            if step == 1:
                # First attempt: try technical solution
                return {
                    "action_type": "technical",
                    "content": "Please reinstall the app from the official store."
                }
            elif step == 2:
                # Second attempt: if still not working, escalate
                return {
                    "action_type": "escalate",
                    "content": "Escalating to senior support team. Ticket ID: ESC-2024-001"
                }
            else:
                # Final step: confirm escalation
                return {
                    "action_type": "escalate",
                    "content": "Senior support has been notified. They will contact you within 2 hours."
                }
    
    def run_task(self, difficulty):
        """Run a single task and output structured results"""
        
        # START block
        print(f"[START] task={difficulty}", flush=True)
        
        # Reset environment
        observation = self.env.reset(difficulty)
        print(f"  Debug: Task message: {observation['message']}", file=sys.stderr)
        
        total_reward = 0.0
        step = 0
        done = False
        max_steps = 3
        
        while not done and step < max_steps:
            # Get action from agent
            action_dict = self.get_action(difficulty, step + 1)
            action = Action(**action_dict)
            
            print(f"  Debug: Step {step+1} - Action: {action.action_type}", file=sys.stderr)
            
            # Execute step
            observation, reward, done, info = self.env.step(action)
            
            step_reward = reward["score"]
            total_reward += step_reward
            step += 1
            
            # STEP block
            print(f"[STEP] step={step} reward={step_reward:.3f}", flush=True)
            print(f"  Debug: Reward reason: {reward['reason']}", file=sys.stderr)
        
        # Calculate final score (ensure between 0 and 1)
        final_score = max(0.001, min(0.999, total_reward / max_steps))
        
        # END block
        print(f"[END] task={difficulty} score={final_score:.3f} steps={step}", flush=True)
        
        return final_score
    
    def run_all_tasks(self):
        """Run all three difficulty levels"""
        results = {}
        
        # Run in specific order
        for difficulty in ["easy", "medium", "hard"]:
            print(f"\n{'='*50}", file=sys.stderr)
            print(f"Running {difficulty.upper()} Task", file=sys.stderr)
            print(f"{'='*50}", file=sys.stderr)
            
            score = self.run_task(difficulty)
            results[difficulty] = score
            
            print(f"  Score: {score:.3f}", file=sys.stderr)
        
        return results

def validate_structured_output(output_lines):
    """Validate that output follows expected format"""
    print("\n" + "="*60, file=sys.stderr)
    print("VALIDATING STRUCTURED OUTPUT", file=sys.stderr)
    print("="*60, file=sys.stderr)
    
    expected_patterns = {
        "START": r"\[START\] task=(easy|medium|hard)",
        "STEP": r"\[STEP\] step=\d+ reward=0\.\d{3}",
        "END": r"\[END\] task=(easy|medium|hard) score=0\.\d{3} steps=\d+"
    }
    
    found_start = False
    found_step = False
    found_end = False
    
    for line in output_lines:
        line = line.strip()
        
        import re
        if re.match(expected_patterns["START"], line):
            found_start = True
            print(f"✓ Valid START block: {line}", file=sys.stderr)
        elif re.match(expected_patterns["STEP"], line):
            found_step = True
            print(f"✓ Valid STEP block: {line}", file=sys.stderr)
        elif re.match(expected_patterns["END"], line):
            found_end = True
            print(f"✓ Valid END block: {line}", file=sys.stderr)
    
    print("\n" + "-"*60, file=sys.stderr)
    if found_start and found_step and found_end:
        print("✅ All structured output blocks are valid!", file=sys.stderr)
        return True
    else:
        print("❌ Missing required structured output blocks:", file=sys.stderr)
        if not found_start:
            print("  - Missing [START] block", file=sys.stderr)
        if not found_step:
            print("  - Missing [STEP] block", file=sys.stderr)
        if not found_end:
            print("  - Missing [END] block", file=sys.stderr)
        return False

def run_comprehensive_test():
    """Run comprehensive test with validation"""
    
    print("\n" + "🚀"*30, file=sys.stderr)
    print("CUSTOMER SUPPORT ENVIRONMENT - MOCK TEST INTERFACE", file=sys.stderr)
    print("🚀"*30, file=sys.stderr)
    
    # Test 1: Environment initialization
    print("\n📋 Test 1: Environment Initialization", file=sys.stderr)
    try:
        env = MyEnvironment()
        print("✅ Environment created successfully", file=sys.stderr)
    except Exception as e:
        print(f"❌ Environment creation failed: {e}", file=sys.stderr)
        return False
    
    # Test 2: Reset with different difficulties
    print("\n📋 Test 2: Reset with Difficulties", file=sys.stderr)
    for difficulty in ["easy", "medium", "hard"]:
        try:
            obs = env.reset(difficulty)
            print(f"✅ Reset '{difficulty}' - Message: {obs['message'][:50]}...", file=sys.stderr)
        except Exception as e:
            print(f"❌ Reset '{difficulty}' failed: {e}", file=sys.stderr)
            return False
    
    # Test 3: Run agent and capture output
    print("\n📋 Test 3: Running Mock Agent", file=sys.stderr)
    
    # Redirect stdout to capture for validation
    from io import StringIO
    import contextlib
    
    stdout_capture = StringIO()
    with contextlib.redirect_stdout(stdout_capture):
        agent = MockAgent()
        results = agent.run_all_tasks()
    
    # Get captured output
    captured_output = stdout_capture.getvalue()
    output_lines = captured_output.split('\n')
    
    # Print captured output (this is what validator sees)
    print("\n" + "="*60, file=sys.stderr)
    print("CAPTURED STDOUT (Validator will see this):", file=sys.stderr)
    print("="*60, file=sys.stderr)
    for line in output_lines:
        if line.strip():
            print(line, file=sys.stderr)
    
    # Validate structured output
    is_valid = validate_structured_output(output_lines)
    
    # Test 4: Verify score ranges
    print("\n📋 Test 4: Score Range Validation", file=sys.stderr)
    all_scores_valid = True
    for difficulty, score in results.items():
        if 0 < score < 1:
            print(f"✅ {difficulty.upper()}: {score:.3f} (within 0-1 range)", file=sys.stderr)
        else:
            print(f"❌ {difficulty.upper()}: {score:.3f} (outside 0-1 range)", file=sys.stderr)
            all_scores_valid = False
    
    # Summary
    print("\n" + "="*60, file=sys.stderr)
    print("TEST SUMMARY", file=sys.stderr)
    print("="*60, file=sys.stderr)
    
    if is_valid and all_scores_valid:
        print("✅ ALL TESTS PASSED!", file=sys.stderr)
        print("\nYour environment is ready for submission!", file=sys.stderr)
        print("\nAverage Score: {:.3f}".format(sum(results.values())/3), file=sys.stderr)
        return True
    else:
        print("❌ SOME TESTS FAILED. Please fix issues above.", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)