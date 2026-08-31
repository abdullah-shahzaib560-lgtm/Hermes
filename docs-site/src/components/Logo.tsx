import Image from "next/image";
import Link from "next/link";

export function Logo({ withWordmark = true }: { withWordmark?: boolean }) {
  return (
    <Link href="/" className="group flex items-center gap-3" aria-label="Hermes home">
      <span className="relative flex h-10 w-10 items-center justify-center overflow-hidden rounded-2xl ring-1 ring-ink/15 transition-transform group-hover:-rotate-6">
        <Image
          src="/Hermes.png"
          alt="Hermes logo"
          width={40}
          height={40}
          className="h-full w-full object-cover"
        />
      </span>
      {withWordmark && (
        <span className="font-heading text-2xl font-bold tracking-tight text-ink">Hermes</span>
      )}
    </Link>
  );
}
