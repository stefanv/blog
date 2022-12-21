.PHONY: github html serve clean

html:
	@hugo
	@touch public/.nojekyll

	@# Default feed contains all posts
	@mv public/atom.xml public/all.xml

	@# Default feed excludes personal category
	@cp public/posts/atom.xml public/atom.xml

serve:
	@hugo --printI18nWarnings server

clean:
	rm -rf public

## A push is now enough to rebuild via Netlify
#
#github: | clean html
#	rm -rf ../mentat/blog && \
#	cp -r public ../mentat/blog && \
#	cd ../mentat && \
#	git add blog && \
#	git ci -m "Blog update" && \
#	git push stefanv master
