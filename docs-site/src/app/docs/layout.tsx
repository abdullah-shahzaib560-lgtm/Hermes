import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { DocsSidebar } from "@/components/DocsSidebar";

export default function DocsLayout({ children }: LayoutProps<"/docs">) {
  return (
    <>
      <Navbar />
      <div className="mx-auto flex w-full max-w-6xl flex-1 px-3 sm:px-4 md:px-6">
        <DocsSidebar />
        <div className="min-w-0 flex-1">
          <div className="mx-auto max-w-3xl px-1 py-8 sm:px-2 sm:py-10 md:px-8 md:py-14">{children}</div>
        </div>
      </div>
      <Footer />
    </>
  );
}
