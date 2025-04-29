"use client";
import React from "react";
import { Inter } from "next/font/google";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

const Hero = () => {
  return (
    <div className={`relative w-full h-[calc(100vh-var(--top-nav-bar-height))] bg-primaryBg flex items-center justify-end ${inter.className}`}>
      {/* Background rectangles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute w-64 h-96 md:w-[575px] md:h-[740px] -left-12 top-60 origin-top-left rotate-[22deg] bg-zinc-300/70"></div>
        <div className="absolute w-60 h-[450px] md:w-[522px] md:h-[796px] left-24 top-72 origin-top-left rotate-[35deg] bg-zinc-300/75"></div>
        <div className="absolute w-96 h-48 md:w-[522px] md:h-[796px] left-64 top-96 origin-top-left rotate-[50deg] bg-zinc-300"></div>
      </div>

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-end gap-8 pr-8 md:pr-72 text-right">
        <h1 className="text-white font-normal text-4xl md:text-7xl leading-tight">
          Resume
          <br />
          Optimizer
        </h1>

        {/* Link as a button */}
        <Link
          href="/login"
          className="w-60 md:w-72 h-12 md:h-16 bg-accentPurple text-black rounded-full text-xl md:text-2xl font-normal flex items-center justify-center cursor-pointer hover:scale-105 transition-transform"
        >
          Get Started
        </Link>
      </div>
    </div>
  );
};

export default Hero;
