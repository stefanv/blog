.PHONY: github html serve clean

html:
	@hugo
	@touch site/public/.nojekyll

serve:
	@hugo --i18n-warnings server -D

clean:
	@rm -rf public

github: html
	rm -rf ../mentat/blog
	cp -r public/* ../mentat/blog
	cd ../mentat && \
	git add blog && \
	git ci -m "Blog update" && \
	git push stefanv master
