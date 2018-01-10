(try
  (let [x 10])
  (except [NameError]
    (try
      (require [hy.extra [let]])
      (except [BaseException]
        (try
          (require [hy.contrib.walk [let]])
          (except [BaseException]
               (defmacro let [] (print "defmacro"))))))))
