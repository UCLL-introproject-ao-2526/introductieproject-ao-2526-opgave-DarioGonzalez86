(defun gen (n &optional (p #'(lambda (x) T)) (k 2))
  (when (<= 0 n)
    (if (funcall p k)
      (cons k
            (gen (1- n)
                 (lambda (x)
                   (and (funcall p x)
                        (not (= 0 (mod x k)))))
                 (1+ k)))
      (gen n p (1+ k)))))

(format T "~{~a~^, ~}" (gen 10))

