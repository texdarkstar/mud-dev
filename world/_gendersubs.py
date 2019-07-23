
import re

# gender maps

_GENDER_PRONOUN_MAP = {"male": {"s": "he",
                                "o": "him",
                                "p": "his",
                                "a": "his"},
                       "female": {"s": "she",
                                  "o": "her",
                                  "p": "her",
                                  "a": "hers"},
                       "neutral": {"s": "it",
                                   "o": "it",
                                   "p": "its",
                                   "a": "its"},
                       "ambiguous": {"s": "they",
                                     "o": "them",
                                     "p": "their",
                                     "a": "theirs"}
                       }
_RE_GENDER_PRONOUN = re.compile(r'(?<!\|)\|(?!\|)[sSoOpPaA]')

    def _get_pronoun(self, regex_match):
        """
        Get pronoun from the pronoun marker in the text. This is used as
        the callable for the re.sub function.

        Args:
            regex_match (MatchObject): the regular expression match.

        Notes:
            - `|s`, `|S`: Subjective form: he, she, it, He, She, It, They
            - `|o`, `|O`: Objective form: him, her, it, Him, Her, It, Them
            - `|p`, `|P`: Possessive form: his, her, its, His, Her, Its, Their
            - `|a`, `|A`: Absolute Possessive form: his, hers, its, His, Hers, Its, Theirs

        """
        typ = regex_match.group()[1]  # "s", "O" etc

        target = None
        gender = "ambiguous"
        if self.db.target:
            target = self.search("#%i" % self.db.target, use_dbref=True, quiet=True).pop()

        if target:
            gender = target.attributes.get("gender", default="ambiguous")

        gender = gender if gender in ("male", "female", "neutral") else "ambiguous"
        pronoun = _GENDER_PRONOUN_MAP[gender][typ.lower()]
        return pronoun.capitalize() if typ.isupper() else pronoun

    def msg(self, text, from_obj=None, session=None, **kwargs):
        """
        Emits something to a session attached to the object.
        Overloads the default msg() implementation to include
        gender-aware markers in output.

        Args:
            text (str, optional): The message to send
            from_obj (obj, optional): object that is sending. If
                given, at_msg_send will be called
            session (Session or list, optional): session or list of
                sessions to relay to, if any. If set, will
                force send regardless of MULTISESSION_MODE.
        Notes:
            `at_msg_receive` will be called on this Object.
            All extra kwargs will be passed on to the protocol.

        """
        # pre-process the text before continuing
        try:
            text = _RE_GENDER_PRONOUN.sub(self._get_pronoun, text)
        except TypeError:
            pass
        super().msg(text, from_obj=from_obj, session=session, **kwargs)