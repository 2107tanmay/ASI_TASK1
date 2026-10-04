// tailwind.config.cjs
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class", // enable class based dark mode
  theme: {
    extend: {
      colors: {
        charcoal: "#1a1a1a",
        accent: "#2563eb", // blue-600
        success: "#10b981", // green-500
        warning: "#f59e0b", // amber-500
        error: "#ef4444", // red-500
      },
    },
  },
  plugins: [],
};
