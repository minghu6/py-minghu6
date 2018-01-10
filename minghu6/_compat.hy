

(defmacro let [bindings &rest body]
  "
sets up lexical bindings in its body

Bindings are processed sequentially,
so you can use the result of an earlier binding in a later one.

Basic assignments (e.g. setv, +=) will update the let binding,
if they use the name of a let binding.

But assignments via `import` are always hoisted to normal Python scope, and
likewise, `defclass` will assign the class to the Python scope,
even if it shares the name of a let binding.

Use __import__ and type (or whatever metaclass) instead,
if you must avoid this hoisting.

Function arguments can shadow let bindings in their body,
as can nested let forms.
"
  (if (odd? (len bindings))
      (macro-error bindings "let bindings must be paired"))
  (setv g!let (gensym 'let)
        replacements (OrderedDict)
        values [])
  (defn expander [symbol]
    (.get replacements symbol symbol))
  (for [[k v] (partition bindings)]
    (if-not (symbol? k)
            (macro-error k "bind targets must be symbols")
            (if (in '. k)
                (macro-error k "binding target may not contain a dot")))
    (.append values (symbolexpand (macroexpand-all v &name) expander))
    (assoc replacements k `(get ~g!let ~(name k))))
  `(do
     (setv ~g!let {}
           ~@(interleave (.values replacements) values))
     ~@(symbolexpand (macroexpand-all body &name) expander)))
