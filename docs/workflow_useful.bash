azd ai eval init          # scaffold the configuration. Makes no service calls
azd ai eval generate      # optional: synthesize a dataset and a rubric evaluator
azd ai eval create        # register the eval in the Foundry project
azd ai eval run start     # run it and summarize the results

# For scripted use, pass the decisions directly:

azd ai eval init \
  --source traces \
  --target support-agent \
  --judge-model gpt-4.1-nano \
  --name support-trace-eval \
  --no-prompt

azd ai eval evaluator list --builtin

# Generate a dataset and an evaluator
azd ai eval generate \
  --target support-agent \
  --generation-model gpt-4.1-nano \
  --agent-instruction "Handles support requests. Test triage, policy adherence, and escalation."
