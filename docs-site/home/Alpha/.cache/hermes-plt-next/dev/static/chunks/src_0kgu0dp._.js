(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/src/components/DocsSidebar.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "DocsSidebar",
    ()=>DocsSidebar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/navigation.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$docs$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/docs.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
;
function DocsSidebar() {
    _s();
    const pathname = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["usePathname"])();
    const [open, setOpen] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const currentSection = __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$docs$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["docsNav"].find((s)=>s.links.some((l)=>pathname.includes(l.href)));
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                onClick: ()=>setOpen((o)=>!o),
                className: "mx-auto mt-6 flex w-[calc(100%-3rem)] items-center justify-center gap-2 rounded-xl border border-line bg-white/60 px-4 py-2.5 font-body text-sm font-semibold shadow-card md:hidden",
                children: [
                    open ? "Close" : "Menu",
                    " · ",
                    currentSection?.title ?? "Docs"
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/DocsSidebar.tsx",
                lineNumber: 19,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("aside", {
                className: `${open ? "block" : "hidden"} md:block md:h-[calc(100vh-65px)] md:sticky md:top-[65px] md:overflow-y-auto md:w-64 md:shrink-0 md:border-r md:border-line/60`,
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("nav", {
                    className: "px-4 py-6 md:px-6 md:py-10",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "mb-8 hidden px-2 font-heading text-xs font-bold uppercase tracking-[0.2em] text-ink-soft/70 md:block",
                            children: "Hermes Docs"
                        }, void 0, false, {
                            fileName: "[project]/src/components/DocsSidebar.tsx",
                            lineNumber: 30,
                            columnNumber: 11
                        }, this),
                        __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$docs$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["docsNav"].map((section)=>{
                            const active = section.links.some((l)=>pathname.includes(l.href));
                            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "mb-8",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: `px-2 font-heading text-sm font-bold ${active ? "text-accent" : "text-ink"}`,
                                        children: section.title
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/DocsSidebar.tsx",
                                        lineNumber: 38,
                                        columnNumber: 17
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                                        className: "mt-2 space-y-0.5",
                                        children: section.links.map((link)=>{
                                            const isActive = pathname === link.href || link.href !== "/docs/overview" && pathname.startsWith(link.href);
                                            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                                    href: link.href,
                                                    onClick: ()=>setOpen(false),
                                                    className: `flex items-center gap-2 rounded-xl px-3 py-2 font-body text-[15px] font-medium transition-colors ${isActive ? "bg-ink text-cream shadow-soft" : "text-ink hover:bg-cream-soft"}`,
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                            className: `h-1.5 w-1.5 rounded-full ${isActive ? "bg-accent" : "bg-line"}`
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/components/DocsSidebar.tsx",
                                                            lineNumber: 59,
                                                            columnNumber: 27
                                                        }, this),
                                                        link.title
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/src/components/DocsSidebar.tsx",
                                                    lineNumber: 50,
                                                    columnNumber: 25
                                                }, this)
                                            }, link.href, false, {
                                                fileName: "[project]/src/components/DocsSidebar.tsx",
                                                lineNumber: 49,
                                                columnNumber: 23
                                            }, this);
                                        })
                                    }, void 0, false, {
                                        fileName: "[project]/src/components/DocsSidebar.tsx",
                                        lineNumber: 43,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, section.title, true, {
                                fileName: "[project]/src/components/DocsSidebar.tsx",
                                lineNumber: 37,
                                columnNumber: 15
                            }, this);
                        }),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                            href: "/",
                            className: "mt-4 flex items-center gap-2 rounded-xl border border-line px-3 py-2 font-body text-sm text-ink transition-colors hover:border-ink",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                    children: "←"
                                }, void 0, false, {
                                    fileName: "[project]/src/components/DocsSidebar.tsx",
                                    lineNumber: 76,
                                    columnNumber: 13
                                }, this),
                                " Back to home"
                            ]
                        }, void 0, true, {
                            fileName: "[project]/src/components/DocsSidebar.tsx",
                            lineNumber: 72,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/components/DocsSidebar.tsx",
                    lineNumber: 29,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/components/DocsSidebar.tsx",
                lineNumber: 26,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/DocsSidebar.tsx",
        lineNumber: 17,
        columnNumber: 5
    }, this);
}
_s(DocsSidebar, "v3TFSdztexVkGEr5cLhcJl2cWfw=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["usePathname"]
    ];
});
_c = DocsSidebar;
var _c;
__turbopack_context__.k.register(_c, "DocsSidebar");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/src/lib/docs.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "docsNav",
    ()=>docsNav
]);
const docsNav = [
    {
        title: "Getting Started",
        links: [
            {
                title: "Overview",
                href: "/docs/overview",
                description: "What Hermes is and why it matters"
            },
            {
                title: "Quickstart",
                href: "/docs/quickstart",
                description: "Install and run your first pipeline"
            }
        ]
    },
    {
        title: "Core Concepts",
        links: [
            {
                title: "Connectors",
                href: "/docs/connectors",
                description: "Every source, one contract"
            },
            {
                title: "Features",
                href: "/docs/features",
                description: "Country risk & financial feature engine"
            }
        ]
    },
    {
        title: "Reference",
        links: [
            {
                title: "API Reference",
                href: "/docs/api-reference",
                description: "The Hermes facade & core objects"
            },
            {
                title: "Roadmap",
                href: "/docs/roadmap",
                description: "Where the platform is headed"
            }
        ]
    }
];
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=src_0kgu0dp._.js.map