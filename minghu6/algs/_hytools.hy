(defn common-set [vars fns] (map (zip vars fns) (fn [self var app] (cond [(none? var) (setattr self 'var var)])))

(defn same [var] var)
