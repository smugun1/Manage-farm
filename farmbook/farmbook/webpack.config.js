const path = require("path");

module.exports = {
  entry: "./src/index.js",  // Your JavaScript entry file
  output: {
    path: path.resolve("static/"),  // Output directory for bundled files
    filename: "main.js",  // Output JavaScript filename
  },
  // Add rules to process your CSS with PostCSS and Tailwind CSS
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          "style-loader",
          "css-loader",
          "postcss-loader",
        ],
      },
    ],
  },
};
