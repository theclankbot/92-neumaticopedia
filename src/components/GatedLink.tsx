
"use client";

import Link from "next/link";
import { ReactNode } from "react";

interface GatedLinkProps {
  href: string;
  published: boolean;
  children: ReactNode;
  className?: string;
  publishedClassName?: string;
  unpublishedClassName?: string;
  title?: string;
}

export default function GatedLink({
  href,
  published,
  children,
  className = "",
  publishedClassName = "",
  unpublishedClassName = "",
  title,
}: GatedLinkProps) {
  if (published) {
    return (
      <Link
        href={href}
        className={`${className} ${publishedClassName}`.trim()}
        title={title}
      >
        {children}
      </Link>
    );
  }

  return (
    <span
      className={`cursor-default ${className} ${unpublishedClassName} text-gray-400`.trim()}
      title={title || "Próximamente"}
      aria-disabled="true"
    >
      {children}
      <span className="ml-1 text-xs bg-gray-200 text-gray-500 px-1.5 py-0.5 rounded-full">
        Próximamente
      </span>
    </span>
  );
}
