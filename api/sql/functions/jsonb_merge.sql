create extension if not exists plv8;

CREATE OR REPLACE FUNCTION public.jsonb_merge(left JSONB, right JSONB)
 returns jsonb
 LANGUAGE plv8
AS $function$

    /* https://gist.github.com/phillip-haydon/54871b746201793990a18717af8d70dc */

    var mergeJSON = function (target, add) {
        function isObject(obj) {
            if (typeof obj == "object") {
                for (var key in obj) {
                    if (obj.hasOwnProperty(key)) {
                        return true; // search for first object prop
                    }
                }
            }
            return false;
        }
        for (var key in add) {
            if (add.hasOwnProperty(key)) {
                if (target[key] && isObject(target[key]) && isObject(add[key])) {
                    mergeJSON(target[key], add[key]);
                } else {
                    target[key] = add[key];
                }
            }
        }
        return target;
    };

    return mergeJSON(left, right);

$function$;
