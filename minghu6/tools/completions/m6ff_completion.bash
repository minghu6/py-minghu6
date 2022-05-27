_m6ff()
{
    local cur ff
    cur="${COMP_WORDS[COMP_CWORD]}"

    if (( $COMP_CWORD == 1 ))
    then
        local tags="cut
                    recompile"

        COMPREPLY=($(compgen -W "${tags}" $cur))
    else
        # get all matching files and directories
        COMPREPLY=($(compgen -f -- "${COMP_WORDS[$COMP_CWORD]}"))

        for ((ff=0; ff<${#COMPREPLY[@]}; ff++)); do
            # [[ -d ${COMPREPLY[$ff]} ]] && COMPREPLY[$ff]+='/'
            [[ -f ${COMPREPLY[$ff]} ]] && COMPREPLY[$ff]+=''
        done
    fi

}
complete -F _m6ff m6ff
