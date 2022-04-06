const webpack = require("webpack");
module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      $env: {
        X_API_KEY: JSON.stringify(process.env.X_API_KEY),
      },
    }),
  ],
};
