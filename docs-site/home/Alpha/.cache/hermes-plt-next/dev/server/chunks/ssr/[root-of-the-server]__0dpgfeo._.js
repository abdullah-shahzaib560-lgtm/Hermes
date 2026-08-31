module.exports = [
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[project]/src/app/docs/quickstart/page.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>QuickstartPage,
    "metadata",
    ()=>metadata
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/Doc.tsx [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/CodeBlock.tsx [app-rsc] (ecmascript)");
;
;
;
const metadata = {
    title: "Quickstart",
    description: "Install hermes-plt and run your first pipeline: instantiate the facade, fetch from a connector, compute features and inspect the cache."
};
const INSTALL_CODE = `pip install hermes-plt`;
const CONSTRUCTOR_CODE = `from hermes import Hermes

hermes = Hermes(
    opensanction_api="",
    new_data_api="",
    fred_api="",
    sec_username="",
    sec_email="",
    finnhub_api="",
    cache_dir=None,   # defaults to ~/.hermes_cache/raw
    use_cache=True,
)`;
const WORLD_BANK_CODE = `import asyncio
from hermes import Hermes

hermes = Hermes(
    opensanction_api="x",
    new_data_api="x",
    sec_username="me@example.com",
    sec_email="me@example.com",
)

# Annual GDP growth (%) for the United States
df = hermes.world_bank.fetch(
    country_code="US",
    indicator_code="NY.GDP.MKTP.KD.ZG",
    frequency="Y",
    per_page=1000,
)

print(df.head())
#       date indicator_id  ...   value   source
# 0  2023-01-01  NY.GDP.MKTP.KD.ZG  ...  2.54  world_bank`;
const FEATURES_CODE = `# Country-risk economic features for the US (mode="F" → scalar)
gdp = await hermes.country_features.get_country_risk_features("USA")

# Or compute a single economic feature directly
growth = await hermes.lf.eco.gdp_growth_yoy(
    country_code="USA",
    mode="F",          # "F" → float, "ML" → pd.Series indexed by year
)

print(growth)  # e.g. 2.54`;
const CACHE_CODE = `stats = hermes.cache_stats()
print(stats)
# {
#   "total_files": 3,
#   "by_source": {"world_bank": 2, "imf": 1},
#   "hits": {"world_bank": 5},
#   "misses": {"world_bank": 2},
#   "hit_rate": {"world_bank": 0.71},
#}

# Purge cached files older than 7 days
hermes.clear_cache(older_than="7d")`;
function QuickstartPage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["DocTitle"], {
                kicker: "Getting Started",
                children: "Quickstart"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 84,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Lead"], {
                children: "Install Hermes, instantiate the facade, fetch data from a connector and compute features — no API keys required for the World Bank source."
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 85,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "1",
                children: "1. Install"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 90,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Hermes requires ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                        children: "Python 3.11 or newer"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 92,
                        columnNumber: 25
                    }, this),
                    ". It is distributed on PyPI as",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "hermes-plt"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 93,
                        columnNumber: 9
                    }, this),
                    ":"
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 91,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                code: INSTALL_CODE,
                title: "terminal"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 95,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Runtime dependencies include ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "aiohttp"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 96,
                        columnNumber: 39
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "pandas"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 96,
                        columnNumber: 61
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "pyarrow"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 97,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "fastparquet"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 97,
                        columnNumber: 31
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "pycountry"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 97,
                        columnNumber: 57
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "pydantic"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 98,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "sdmx"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 98,
                        columnNumber: 32
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "sec-cik-mapper"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 98,
                        columnNumber: 51
                    }, this),
                    " and",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "yfinance"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 99,
                        columnNumber: 9
                    }, this),
                    " — installed automatically."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 96,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "2",
                children: "2. Instantiate the facade"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 102,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "The ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "Hermes"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 104,
                        columnNumber: 13
                    }, this),
                    " class is the single entry point. Its constructor takes the API credentials it may need and sets up a shared cache:"
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 103,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                code: CONSTRUCTOR_CODE,
                title: "python"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 107,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Callout"], {
                title: "KeyError guard",
                tone: "gold",
                children: [
                    "The constructor raises ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "KeyError"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 109,
                        columnNumber: 32
                    }, this),
                    " if both ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "opensanction_api"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 109,
                        columnNumber: 62
                    }, this),
                    " and",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "new_data_api"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 110,
                        columnNumber: 9
                    }, this),
                    " are empty. Pass any placeholder to proceed — only connectors you actually use need real keys."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 108,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Setting ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "use_cache=False"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 114,
                        columnNumber: 17
                    }, this),
                    " disables the ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "RawCache"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 114,
                        columnNumber: 59
                    }, this),
                    "; otherwise all connectors share one ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "RawCache(cache_dir)"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 115,
                        columnNumber: 30
                    }, this),
                    "."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 113,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "3",
                children: "3. Fetch a dataset"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 118,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Connectors are async (built on ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "aiohttp"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 120,
                        columnNumber: 40
                    }, this),
                    " with exponential-backoff retries). Pull annual GDP growth for the US from the World Bank:"
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 119,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                code: WORLD_BANK_CODE,
                title: "python"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 123,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "The returned DataFrame follows the canonical connector schema:",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "date, indicator_id, indicator_name, country, value, source"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 126,
                        columnNumber: 9
                    }, this),
                    ". Flag",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "force=True"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 127,
                        columnNumber: 9
                    }, this),
                    " to bypass the cache for a fresh pull."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 124,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "4",
                children: "4. Compute country-risk features"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 130,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Feed a country through the country-risk pipeline to derive intelligence across all five feature groups. Each feature accepts ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: 'mode="F"'
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 133,
                        columnNumber: 46
                    }, this),
                    " (latest scalar) or",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: 'mode="ML"'
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 134,
                        columnNumber: 9
                    }, this),
                    " (a ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "pd.Series"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 134,
                        columnNumber: 45
                    }, this),
                    " indexed by year 2000–2025, forward-filled):"
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 131,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                code: FEATURES_CODE,
                title: "python"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 136,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "5",
                children: "5. Inspect the cache"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 138,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: "Check per-source hit/miss statistics and purge entries older than a threshold:"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 139,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                code: CACHE_CODE,
                title: "python"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 140,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Callout"], {
                title: "Cache path",
                tone: "cedar",
                children: [
                    "Files live under ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "~/.hermes_cache/raw/<source>/<hash>.parquet"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 142,
                        columnNumber: 26
                    }, this),
                    " with a",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: ".meta.json"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 143,
                        columnNumber: 9
                    }, this),
                    " sidecar. Keys are a 16-char ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "sha256"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 143,
                        columnNumber: 61
                    }, this),
                    " of the source plus sorted JSON params."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 141,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "env",
                children: "Environment variables"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 147,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Copy ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: ".env.example"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 149,
                        columnNumber: 14
                    }, this),
                    " to ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: ".env"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 149,
                        columnNumber: 43
                    }, this),
                    " and fill in the keys used by the connectors you need:"
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 148,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: ".env",
                code: `OPEN_SANCTIONS_API=
NEWS_DATA_API=
FRED_API=
FINNHUB_API=
SEC_USERNAME=
SEC_EMAIL=`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 152,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Variable",
                    "Used by"
                ],
                rows: [
                    [
                        "OPEN_SANCTIONS_API",
                        "OpenSanctions connector"
                    ],
                    [
                        "NEWS_DATA_API",
                        "OpenSanctions connector"
                    ],
                    [
                        "FRED_API",
                        "FRED connector (macro series)"
                    ],
                    [
                        "FINNHUB_API",
                        "Finnhub connector + financial features"
                    ],
                    [
                        "SEC_USERNAME / SEC_EMAIL",
                        "SEC EDGAR connector (User-Agent)"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 161,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "next",
                children: "Next steps"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 172,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Browse the ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["DocLink"], {
                        href: "/docs/connectors",
                        children: "connectors"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 174,
                        columnNumber: 20
                    }, this),
                    ", learn the",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["DocLink"], {
                        href: "/docs/features",
                        children: "feature engine"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 175,
                        columnNumber: 9
                    }, this),
                    ", or dive into the",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["DocLink"], {
                        href: "/docs/api-reference",
                        children: "API reference"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/quickstart/page.tsx",
                        lineNumber: 176,
                        columnNumber: 9
                    }, this),
                    "."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 173,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["PrevNext"], {
                prev: {
                    title: "Overview",
                    href: "/docs/overview"
                },
                next: {
                    title: "Connectors",
                    href: "/docs/connectors"
                }
            }, void 0, false, {
                fileName: "[project]/src/app/docs/quickstart/page.tsx",
                lineNumber: 179,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/app/docs/quickstart/page.tsx",
        lineNumber: 83,
        columnNumber: 5
    }, this);
}
}),
"[project]/src/app/docs/quickstart/page.tsx [app-rsc] (ecmascript, Next.js Server Component)", (function(__turbopack_context__){

__turbopack_context__.n(__turbopack_context__.i("[project]/src/app/docs/quickstart/page.tsx [app-rsc] (ecmascript)"));
}),
"[project]/src/app/favicon.ico (static in ecmascript, tag client)", ((__turbopack_context__) => {

__turbopack_context__.v("/_next/static/media/favicon.2vob68tjqpejf.ico" + (globalThis["NEXT_CLIENT_ASSET_SUFFIX"] || ''));}),
"[project]/src/app/favicon.ico.mjs { IMAGE => \"[project]/src/app/favicon.ico (static in ecmascript, tag client)\" } [app-rsc] (structured image object, ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$app$2f$favicon$2e$ico__$28$static__in__ecmascript$2c$__tag__client$29$__ = __turbopack_context__.i("[project]/src/app/favicon.ico (static in ecmascript, tag client)");
;
const __TURBOPACK__default__export__ = {
    src: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$app$2f$favicon$2e$ico__$28$static__in__ecmascript$2c$__tag__client$29$__["default"],
    width: 256,
    height: 256
};
}),
"[project]/src/components/CodeBlock.tsx [app-rsc] (client reference proxy)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "CodeBlock",
    ()=>CodeBlock
]);
// This file is generated by next-core EcmascriptClientReferenceModule.
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$server$2d$dom$2d$turbopack$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-server-dom-turbopack-server.js [app-rsc] (ecmascript)");
;
const CodeBlock = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$server$2d$dom$2d$turbopack$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["registerClientReference"])(function() {
    throw new Error("Attempted to call CodeBlock() from the server but CodeBlock is on the client. It's not possible to invoke a client function from the server, it can only be rendered as a Component or passed to props of a Client Component.");
}, "[project]/src/components/CodeBlock.tsx", "CodeBlock");
}),
"[project]/src/components/CodeBlock.tsx [app-rsc] (client reference proxy) <module evaluation>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "CodeBlock",
    ()=>CodeBlock
]);
// This file is generated by next-core EcmascriptClientReferenceModule.
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$server$2d$dom$2d$turbopack$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-server-dom-turbopack-server.js [app-rsc] (ecmascript)");
;
const CodeBlock = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$server$2d$dom$2d$turbopack$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["registerClientReference"])(function() {
    throw new Error("Attempted to call CodeBlock() from the server but CodeBlock is on the client. It's not possible to invoke a client function from the server, it can only be rendered as a Component or passed to props of a Client Component.");
}, "[project]/src/components/CodeBlock.tsx <module evaluation>", "CodeBlock");
}),
"[project]/src/components/CodeBlock.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$client__reference__proxy$29$__$3c$module__evaluation$3e$__ = __turbopack_context__.i("[project]/src/components/CodeBlock.tsx [app-rsc] (client reference proxy) <module evaluation>");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$client__reference__proxy$29$__ = __turbopack_context__.i("[project]/src/components/CodeBlock.tsx [app-rsc] (client reference proxy)");
;
__turbopack_context__.n(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$client__reference__proxy$29$__);
}),
"[project]/src/components/Doc.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Callout",
    ()=>Callout,
    "DocLink",
    ()=>DocLink,
    "DocTitle",
    ()=>DocTitle,
    "H2",
    ()=>H2,
    "Lead",
    ()=>Lead,
    "List",
    ()=>List,
    "P",
    ()=>P,
    "PrevNext",
    ()=>PrevNext,
    "Table",
    ()=>Table
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.react-server.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/Doodle.tsx [app-rsc] (ecmascript)");
;
;
;
function DocTitle({ children, kicker }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "mb-8",
        children: [
            kicker && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-3 inline-flex items-center gap-2 rounded-full border border-line bg-white/60 px-3 py-1 font-body text-xs font-bold uppercase tracking-wider text-accent",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Sparkle"], {
                        className: "h-3.5 w-3.5",
                        color: "#ff4126",
                        strokeWidth: 4
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 9,
                        columnNumber: 11
                    }, this),
                    kicker
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 8,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                className: "font-heading text-4xl font-extrabold tracking-tight text-ink md:text-5xl",
                children: children
            }, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 13,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 6,
        columnNumber: 5
    }, this);
}
function H2({ children, id }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
        id: id,
        className: "mt-12 mb-4 flex items-center gap-3 font-heading text-2xl font-extrabold tracking-tight text-ink",
        children: [
            children,
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Sparkle"], {
                className: "h-5 w-5 opacity-60",
                color: "#ff4126",
                strokeWidth: 4
            }, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 27,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 22,
        columnNumber: 5
    }, this);
}
function P({ children }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        className: "my-4 font-body text-[16.5px] leading-relaxed text-ink",
        children: children
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 33,
        columnNumber: 10
    }, this);
}
function Lead({ children }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        className: "mb-6 text-lg font-body leading-relaxed text-ink",
        children: children
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 38,
        columnNumber: 5
    }, this);
}
function List({ items }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
        className: "dot-bullet my-4 space-y-2.5",
        children: items.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                className: "font-body text-[16.5px] text-ink",
                children: item
            }, item, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 46,
                columnNumber: 9
            }, this))
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 44,
        columnNumber: 5
    }, this);
}
function Callout({ title, children, tone = "accent" }) {
    const map = {
        accent: {
            bg: "#ff4126",
            label: "Note"
        },
        cedar: {
            bg: "#1f5f4b",
            label: "Tip"
        },
        gold: {
            bg: "#b88a1f",
            label: "Warning"
        }
    };
    const t = map[tone];
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "my-6 overflow-hidden rounded-2xl border border-line bg-white",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-2 px-4 py-2.5",
                style: {
                    backgroundColor: `${t.bg}`
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Sparkle"], {
                        className: "h-4 w-4 text-white",
                        color: "#fff",
                        strokeWidth: 4
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 72,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "font-heading text-sm font-bold text-white",
                        children: title
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 73,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 71,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "px-5 py-4 font-body text-[15px] leading-relaxed text-ink",
                children: children
            }, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 75,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 70,
        columnNumber: 5
    }, this);
}
function DocLink({ href, children, external }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
        href: href,
        target: external ? "_blank" : undefined,
        rel: external ? "noopener noreferrer" : undefined,
        className: "font-medium text-accent underline decoration-accent/40 underline-offset-4 transition-colors hover:text-accent-dark hover:decoration-accent",
        children: children
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 82,
        columnNumber: 5
    }, this);
}
function PrevNext({ prev, next }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "mt-14 grid gap-4 border-t border-line/70 pt-8 sm:grid-cols-2",
        children: [
            prev ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                href: prev.href,
                className: "group rounded-2xl border border-line bg-white p-5 transition-all hover:-translate-y-0.5 hover:shadow-card",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "font-body text-xs uppercase tracking-wider text-ink-soft",
                        children: "← Previous"
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 101,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mt-1 font-heading font-bold text-ink group-hover:text-accent",
                        children: prev.title
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 102,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 97,
                columnNumber: 9
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {}, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 105,
                columnNumber: 9
            }, this),
            next ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                href: next.href,
                className: "group rounded-2xl border border-line bg-white p-5 text-right transition-all hover:-translate-y-0.5 hover:shadow-card",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "font-body text-xs uppercase tracking-wider text-ink-soft",
                        children: "Next →"
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 112,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mt-1 font-heading font-bold text-ink group-hover:text-accent",
                        children: next.title
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 113,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 108,
                columnNumber: 9
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {}, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 116,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 95,
        columnNumber: 5
    }, this);
}
function Table({ head, rows }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "my-6 overflow-x-auto rounded-2xl border border-line bg-white",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("table", {
            className: "w-full text-left font-body text-[15px]",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("thead", {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                        className: "border-b border-line bg-cream-soft/70",
                        children: head.map((h)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                className: "px-4 py-3 font-heading text-sm font-bold text-ink",
                                children: h
                            }, h, false, {
                                fileName: "[project]/src/components/Doc.tsx",
                                lineNumber: 129,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 127,
                        columnNumber: 11
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/src/components/Doc.tsx",
                    lineNumber: 126,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("tbody", {
                    children: rows.map((row, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                            className: "border-b border-line/50 last:border-0",
                            children: row.map((cell, j)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                    className: "px-4 py-3 align-top text-ink",
                                    children: cell
                                }, j, false, {
                                    fileName: "[project]/src/components/Doc.tsx",
                                    lineNumber: 139,
                                    columnNumber: 17
                                }, this))
                        }, i, false, {
                            fileName: "[project]/src/components/Doc.tsx",
                            lineNumber: 137,
                            columnNumber: 13
                        }, this))
                }, void 0, false, {
                    fileName: "[project]/src/components/Doc.tsx",
                    lineNumber: 135,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/src/components/Doc.tsx",
            lineNumber: 125,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 124,
        columnNumber: 5
    }, this);
}
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__0dpgfeo._.js.map