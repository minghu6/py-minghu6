(import [re [sub IGNORECASE]])

(defn arrow-to-to [name]
  (sub "([a-z_]\w*)->(\w*)" r"\1_to_\2" name :flags IGNORECASE))

(defn camelcase->snakecase [name]
  (->> (sub "([A-Z]+)([A-Z][a-z0-9])" r"\1_\2" name)
       (sub "([a-z0-9])([A-Z])" r"\1_\2")
       (.lower)))
