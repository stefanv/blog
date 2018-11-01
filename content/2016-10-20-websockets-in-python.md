Title: WebSockets in Python (and some Redux)
Tags: web, python, javascript, websocket, redux, react
Status: published

As part of our work on [Cesium](http://cesium.ml) and its
[web frontend](https://github.com/cesium-ml/cesium_web),
we've developed an easy
mechanism for Python web developers to
[push messages from their Python backends to the browser](http://cesium.ml/blog/2016/07/13/a-pattern-for-websockets-in-python/).
<!-- PELICAN_END_SUMMARY -->

There are plenty of potential use cases, but consider, e.g., that you want
to verify a credit card number submitted by your user.  Traditionally, you'd
submit the number, and then poll the backend repeatedly from the browser.  Not
very elegant :/

But with a WebSocket connection, you submit the credit card number and then
forget about it.  The *server* will let you know when it's done by pushing a
message to the frontend.

Not only does this solve the annoying polling problem, but it opens up the
door to an entirely new universe of tools, such as Dan Abramov's fantastic
[Redux](http://redux.js.org/).  Many of these Javascript libraries rely on the server
being able to notify the frontend when it needs to update itself.

Let's talk a bit about Redux.  The
[principles](http://redux.js.org/docs/introduction/ThreePrinciples.html)
behind it are simple and elegant:

1. The entire state of your app is centrally
stored (in the equivalent of a Python dictionary);
2. the state is immutable, and
3. can only be updated through a central function call.

That centralization in turn enables other features such as logging, hot
reloading, time travel, etc.

One of the great joys of Redux lies in moving away from the traditional
Model-View-Controller pattern.  With MVC, you are never quite sure how changes
propagate through the system.  With Redux, it is highly predictable.  Say
your app has a toggle button, and associated state `{toggle: true}`.  An
action (e.g. "the red button was clicked") is submitted to the central
dispatcher which then calculates the new state of the app:

```javascript
new_state = reduce(current_state, action)
```

The implementation could look something like this:

```javascript
function reduce(current_state, action) {
  switch (action.type) {
    case 'toggle_button':
      return {toggle: !current_state.toggle}
    default:
      return current_state;
  }
}
```

The toggle button monitors the app state, and when `state['toggle']` is
updated, re-renders itself.

By vastly simplifying flow of information, by
[disentangling mutation and asynchronicity](http://redux.js.org/docs/introduction/Motivation.html), and by
getting rid of JQuery & hidden state stored somewhere in the bowels of the DOM,
Redux has, for me, returned the joy of web development.

But, I'm getting distracted.  WebSockets---in Python!

Pushing messages from your Python web server to the user's browser can now be
[as simple as this](https://github.com/cesium-ml/cesium_web/blob/e19e5543e193905da9555ce15fc71a52859c9fb0/cesium_app/handlers/base.py#L59):

```python
from Flow import flow

self.flow.push('my_user@domain.com', 'message to the user',
               {'data': 'to ship along'})
```

Please take a look at the more detailed technical description (with code!)
[on the Cesium blog](http://cesium.ml/blog/2016/07/13/a-pattern-for-websockets-in-python/).
