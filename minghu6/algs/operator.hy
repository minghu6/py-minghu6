(defn getitem [iterable index &optional default]
  (try
    (get iterable index)
    (except
      [e [IndexError KeyError TypeError]]
      (cond [(none? default) (raise e)]
            [default]))))

(defn c-not [var]
  (cond [(none? var) 0])
  (cond [(numeric? var)
         (cond [(zero? var) 0]
               [1])]))
