from pyasn1.type import univ, char, constraint, namedtype


class FrogTip(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('number', univ.Integer()),
        namedtype.NamedType('tip', char.UTF8String()),
    )

    @staticmethod
    def from_tip(tip):
        return FrogTip().setComponents(tip['number'], tip['tip'])


class Croak(univ.SequenceOf):
    componentType = FrogTip()
    subtypeSpec = constraint.ValueSizeConstraint(0, 50)

    @staticmethod
    def from_tips(tips):
        components = map(FrogTip.from_tip, tips)
        return Croak().setComponents(*components)
