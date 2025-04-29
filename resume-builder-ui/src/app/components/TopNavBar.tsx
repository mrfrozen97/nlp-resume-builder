"use client";
import { usePathname } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import logoSrc from "public/logo.svg";
import { cx } from "lib/cx";

export const TopNavBar = () => {
  const pathName = usePathname();
  const isHomePage = pathName === "/";
  
  return (
    <header
      aria-label="Site Header"
      className={cx(
        "flex h-[var(--top-nav-bar-height)] items-center border-b-2 border-gray-100 px-3 lg:px-12 w-full",
        isHomePage && "bg-dot"
      )}
    >
      <div className="flex h-10 w-full items-center justify-between">
        <Link href="/">
          <span className="sr-only">NLP Resume Builder</span>
          <div className="flex items-center font-medium">
            <Image
              src={logoSrc}
              alt="OpenResume Logo"
              className="h-8"
              priority
              width={50}
              height={32}
            />
            <h2 className="ml-2 block text-base md:text-lg">NLP Resume Builder</h2>
          </div>
        </Link>
        
        <nav
          aria-label="Site Nav Bar"
          className="flex items-center gap-1 text-sm font-medium"
        >
          {/* Add your page to the list below */}
          {[
            ["/resume-builder", "Builder"],
            ["/resume-parser", "Upload"],
            ["/resume-evaluation", "Evaluation"],
                      ].map(([href, text]) => (
            <Link
              key={text}
              className="rounded-md px-1 py-1.5 text-gray-500 hover:bg-gray-100 focus-visible:bg-gray-100 lg:px-3"
              href={href}
            >
              {text}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
};