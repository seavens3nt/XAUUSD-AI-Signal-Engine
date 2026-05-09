import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        panel: "#121821",
        line: "#253143",
        gold: "#f3c969",
        ink: "#e6edf5"
      }
    }
  },
  plugins: []
};

export default config;
