/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/app/**/*.{ts,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        primaryBg: '#4C4967',
        accentPurple: '#9033CE',
      },
    },
  },
  corePlugins: {
    aspectRatio: false,
  },
  plugins: [
    require("tailwind-scrollbar")({ nocompatible: true }),
    require("@tailwindcss/aspect-ratio"),
  ],
};
