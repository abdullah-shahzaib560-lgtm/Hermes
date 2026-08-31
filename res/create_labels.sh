#!/usr/bin/env bash

set -e

# Target repository configuration
TARGET_REPO="ryomenhaider/Hermes"

# 1. Verification checks
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI ('gh') is not installed."
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo "❌ Error: Not authenticated. Please run 'gh auth login' first."
    exit 1
fi

# 2. Define labels grouped by category (Format: "NAME|HEX_COLOR|DESCRIPTION")
LABELS=(
    # --- TYPE LABELS (Blue/Action shades) ---
    "type:feature|a2eeef|New functional capabilities or features"
    "type:bug|d73a4a|Something isn't working as intended"
    "type:refactor|d4c5f9|Code changes that neither fix a bug nor add a feature"
    "type:test|e99695|Adding missing tests or correcting existing tests"
    "type:documentation|0075ca|Improvements or additions to documentation"
    "type:research|bfdadc|Spikes, investigations, or academic research"

    # --- AREA LABELS (Purple/Domain shades) ---
    "area:core|c5def5|Changes impacting the foundational codebase"
    "area:connector|bfd4f2|Integrations, plugins, and third-party links"
    "area:parser|f9d0c4|Syntax, semantic parsing, and lexing logic"
    "area:normalization|dfbbf2|Data formatting and structural standardization"
    "area:validation|1d76db|Input validation and schema enforcement rules"
    "area:metadata|b60205|Data attributes, properties, and definitions"
    "area:entity|5319e7|Data models, entities, and business domains"
    "area:storage|e11d21|Database schemas, file systems, and persistence layers"
    "area:query|006b75|Querying engine, indexing, and lookup operations"

    # --- DIFFICULTY LABELS (Progressive Heat Map: Green to Dark Red) ---
    "difficulty:beginner|70e000|Good for newcomers; minimal context required"
    "difficulty:easy|38b000|Straightforward tasks requiring basic codebase knowledge"
    "difficulty:medium|ffb703|Standard engineering task requiring moderate familiarity"
    "difficulty:hard|fb8500|Complex logic or large architectural impacts"
    "difficulty:architecture|d90429|High-level design structural refactoring or paradigms"
)

echo "🚀 Starting bulk label creation for repo: $TARGET_REPO..."

# 3. Process and create each label
for item in "${LABELS[@]}"; do
    IFS="|" read -r name color description <<< "$item"
    
    echo "----------------------------------------"
    echo "Creating/Updating label: '$name' [#$color] in $TARGET_REPO"
    
    # Explicitly targeting the ryomenhaider/Hermes repo
    gh label create "$name" \
        --repo "$TARGET_REPO" \
        --color "$color" \
        --description "$description" \
        --force
done

echo "----------------------------------------"
echo "🎉 All labels successfully pushed to ryomenhaider/Hermes!"

