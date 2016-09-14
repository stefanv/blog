If Pelican won't find Markdown content, do

```
pip install Markdown
```

Download submodule dependencies with:

```
git submodule init
git submodule update
```

The theme is from

github.com/duilio/pelican-octopress-theme.git

I like Solarized with the light code theme, so had to modify the file
``sass/base/_solarized.scss``:

```
$solarized: light !default;
```

and then recompile the theme using ``compass compile``.

To publish on mentat.za.net:

1. make upload
