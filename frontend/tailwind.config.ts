import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        csu: {
          green:      "#0d4f2e",
          "green-dk": "#093d23",
          "green-lt": "#6abf69",
        },
      },
    },
  },
  plugins: [],
};

export default config;
