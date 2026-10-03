# ~/.config/zsh/girih.zsh-theme
# Girih prompt: agnoster's segment chain, recoloured, standalone (no oh-my-zsh).
#   status  Red, only on failure / root / background jobs
#   context Raised Slate + Brass, only over SSH or as another user
#   dir     Lapis + Ivory
#   git     Emerald when clean, Brass with ± when dirty; branch glyph ◇
# Hex colours need zsh 5.7+ and a true-colour terminal; the arrow needs a Nerd Font.

setopt prompt_subst

GIRIH_DEFAULT_USER=${GIRIH_DEFAULT_USER:-rahal}   # hide context on your own box

G_SLATE='#1A2233' G_LAPIS='#1F4E9C' G_EMERALD='#0F6B4F'
G_BRASS='#C9A24A' G_GOLD='#E6C36A'  G_IVORY='#F2EAD8'
G_RED='#C0503F'   G_OBS='#0B0E14'   G_HAIR='#2A3345'

GIRIH_SEP=$'\ue0b0'
typeset -g GIRIH_BG=NONE

girih_segment() {
  local bg="%K{$1}" fg="%F{$2}"
  if [[ $GIRIH_BG != NONE && $1 != $GIRIH_BG ]]; then
    print -n "%{$bg%F{$GIRIH_BG}%}$GIRIH_SEP%{$fg%} "
  else
    print -n "%{$bg%}%{$fg%} "
  fi
  GIRIH_BG=$1
  [[ -n $3 ]] && print -n -- "$3 "
}

girih_end() {
  if [[ $GIRIH_BG != NONE ]]; then
    print -n "%{%k%F{$GIRIH_BG}%}$GIRIH_SEP"
  else
    print -n "%{%k%}"
  fi
  print -n "%{%f%}"
  GIRIH_BG=NONE
}

# ~/dotfiles/hypr -> ~/d/hypr
girih_short_pwd() {
  local p=${(%):-%~}
  local -a parts=("${(@s:/:)p}")
  local i
  for (( i = 1; i < ${#parts}; i++ )); do
    [[ -z ${parts[i]} || ${parts[i]} == '~' ]] && continue
    if [[ ${parts[i]} == .* ]]; then
      parts[i]=${parts[i][1,2]}
    else
      parts[i]=${parts[i][1]}
    fi
  done
  print -rn -- "${(j:/:)parts//\%/%%}"
}

girih_status() {
  local -a s
  (( GIRIH_RETVAL != 0 )) && s+="✘ $GIRIH_RETVAL"
  (( UID == 0 )) && s+="%F{$G_GOLD}⚡%F{$G_IVORY}"
  [[ -n ${jobstates} ]] && s+="%F{$G_GOLD}⚙%F{$G_IVORY}"
  (( ${#s} )) && girih_segment $G_RED $G_IVORY "${(j: :)s}"
}

girih_context() {
  [[ $USER != $GIRIH_DEFAULT_USER || -n $SSH_CONNECTION ]] &&
    girih_segment $G_SLATE $G_BRASS '%n@%m'
}

girih_dir() {
  girih_segment $G_LAPIS $G_IVORY "$(girih_short_pwd)"
}

girih_git() {
  command git rev-parse --is-inside-work-tree &>/dev/null || return
  local ref
  ref=$(command git symbolic-ref --short HEAD 2>/dev/null) ||
    ref="➦ $(command git rev-parse --short HEAD 2>/dev/null)"
  ref=${ref//\%/%%}
  if [[ -n $(command git status --porcelain --ignore-submodules=dirty 2>/dev/null | head -n1) ]]; then
    girih_segment $G_BRASS $G_OBS "◇ $ref ±"
  else
    girih_segment $G_EMERALD $G_IVORY "◇ $ref"
  fi
}

girih_build_prompt() {
  girih_status
  girih_context
  girih_dir
  girih_git
  girih_end
}

girih_precmd() { GIRIH_RETVAL=$? }
autoload -Uz add-zsh-hook
add-zsh-hook precmd girih_precmd

PROMPT='%{%f%b%k%}$(girih_build_prompt) '
RPROMPT="%F{$G_HAIR}%*%f"

# ---- completion ------------------------------------------------------
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors 'ma=48;2;26;34;51;38;2;242;234;216'

# ---- plugins ---------------------------------------------------------
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=$G_HAIR"
[[ -r /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]] &&
  source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# zsh-syntax-highlighting must be sourced last, then styled.
if [[ -r /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
  source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  ZSH_HIGHLIGHT_STYLES[command]='fg=#2E9C6F'
  ZSH_HIGHLIGHT_STYLES[builtin]='fg=#2E9C6F'
  ZSH_HIGHLIGHT_STYLES[alias]='fg=#2E9C6F'
  ZSH_HIGHLIGHT_STYLES[function]='fg=#2E9C6F'
  ZSH_HIGHLIGHT_STYLES[precommand]='fg=#2E9C6F,underline'
  ZSH_HIGHLIGHT_STYLES[path]='fg=#F2EAD8'
  ZSH_HIGHLIGHT_STYLES[single-hyphen-option]='fg=#3FA8A0'
  ZSH_HIGHLIGHT_STYLES[double-hyphen-option]='fg=#3FA8A0'
  ZSH_HIGHLIGHT_STYLES[single-quoted-argument]='fg=#E6C36A'
  ZSH_HIGHLIGHT_STYLES[double-quoted-argument]='fg=#E6C36A'
  ZSH_HIGHLIGHT_STYLES[unknown-token]='fg=#C0503F,underline'
fi

export FZF_DEFAULT_OPTS="--color=bg+:#1A2233,fg:#A8A090,fg+:#F2EAD8,hl:#C9A24A,hl+:#E6C36A,pointer:#E6C36A,prompt:#E6C36A,info:#C9A24A,border:#C9A24A --pointer='◆' --border=sharp"
