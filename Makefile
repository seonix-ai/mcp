# Seonix plugin - validation and packaging.
#
#   make validate   # JSON syntax + claude plugin validate + Agent Plugins schema checks
#   make codex-zip  # dist/seonix-codex-plugin.zip for the OpenAI submission portal
#   make clean      # remove dist/

.PHONY: validate validate-claude validate-schemas validate-json codex-zip clean

PLUGIN := plugins/seonix

JSON_FILES := .claude-plugin/marketplace.json .agents/plugins/marketplace.json \
	.cursor-plugin/marketplace.json .cursor/mcp.json \
	$(PLUGIN)/plugin.json $(PLUGIN)/mcp.json $(PLUGIN)/.mcp.json \
	$(PLUGIN)/.claude-plugin/plugin.json $(PLUGIN)/.codex-plugin/plugin.json \
	$(PLUGIN)/.cursor-plugin/plugin.json

validate: validate-json validate-claude validate-schemas

validate-json:
	@for f in $(JSON_FILES); do python3 -I -c "import json,sys; json.load(open(sys.argv[1]))" $$f && echo "OK   $$f"; done

# The marketplace run also validates the relative-path plugin's manifest;
# the second run validates the plugin directory on its own (skills included).
validate-claude:
	claude plugin validate --strict .
	claude plugin validate --strict $(PLUGIN)

validate-schemas:
	python3 -I scripts/validate-schemas.py

codex-zip:
	bash scripts/build-codex-zip.sh

clean:
	rm -rf dist
