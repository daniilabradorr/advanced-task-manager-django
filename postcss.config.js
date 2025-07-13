module.exports = {
  plugins: [
    require('@fullhuman/postcss-purgecss')({
      content: [
        './templates/**/*.html',
        './**/templates/**/*.html',
        './static/js/**/*.js'
      ],
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
    })
  ]
};
