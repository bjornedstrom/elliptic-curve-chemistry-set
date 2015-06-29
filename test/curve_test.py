# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import unittest
from field import Field
from curve import ShortWeierstrass, MontgomeryCurve, EdwardsCurve, TwistedEdwardsCurve, montgomery_ladder, montgomery_ladder_projective


class CommonCurveTestsMixin(object):
    def test_group_law_commutativity(self):
        self.assertEquals(self.AplusB, self.curve.add_points(self.A, self.B))
        self.assertEquals(self.AplusB, self.curve.add_points(self.B, self.A))

    def test_multiplication_by_0(self):
        self.assertEquals(self.curve.neutral_point(), montgomery_ladder(0, self.A, self.curve))

    def test_multiplication_by_1_equals_self(self):
        self.assertEquals(self.A, montgomery_ladder(1, self.A, self.curve))

    def test_multiplication_by_2_equals_doubling(self):
        self.assertEquals(self.curve.double_point(self.A), montgomery_ladder(2, self.A, self.curve))

    def test_addition_common(self):
        self.assertEquals(self.AplusB, self.curve.add_points(self.A, self.B))

    def test_double_common(self):
        self.assertEquals(self.Ax2, self.curve.double_point(self.A))

    #def test_addition_A_plus_A_equals_doubling_A(self):
    #    self.assertEquals(self.Ax2, self.curve.add_points(self.A, self.A))

    def test_multiplication_by_1(self):
        self.assertEquals(self.A, montgomery_ladder(1, self.A, self.curve))

    def test_invert_point(self):
        self.assertEquals(self.negB, self.curve.invert_point(self.B))

    def test_valid_point_on_curve(self):
        self.assertTrue(self.curve.point_on_curve(self.A))

    def test_invalid_point_on_curve(self):
        self.assertTrue(not self.curve.point_on_curve((self.A[0], self.A[1]+1)))

    def test_addition_with_infinity(self):
        if self.HAS_INF:
            self.assertEquals(None, self.curve.add_points(None, None))
            self.assertEquals(self.A, self.curve.add_points(self.A, None))
            self.assertEquals(self.A, self.curve.add_points(None, self.A))

    def test_doubling_with_infinity(self):
        if self.HAS_INF:
            self.assertEquals(None, self.curve.double_point(None))

    def test_multiplication(self):
        self.assertEquals(self.MUL_P_1, montgomery_ladder(self.MUL_K_1, self.bp, self.curve))
        self.assertEquals(self.MUL_P_2, montgomery_ladder(self.MUL_K_2, self.bp, self.curve))


class ProjectiveCoordinateTestsMixin(object):
    def test_projective_single_addition(self):
        Aproj = self.curve.affine_to_projective(self.A)
        Bproj = self.curve.affine_to_projective(self.B)

        apb = self.curve.add_points_projective(Aproj, Bproj)

        self.assertEquals(self.AplusB, self.curve.projective_to_affine(apb))

    def test_projective_single_doubling(self):
        Aproj = self.curve.affine_to_projective(self.A)

        ax2 = self.curve.double_point_projective(Aproj)

        self.assertEquals(self.Ax2, self.curve.projective_to_affine(ax2))

    def test_projective_convert_infinity(self):
        if self.HAS_INF:
            self.assertEquals((0, 1, 0), self.curve.affine_to_projective(None))

            self.assertEquals(None, self.curve.projective_to_affine((0, 1, 0)))

    def test_projective_add_infinity(self):
        if self.HAS_INF:
            NP = self.curve.neutral_point_projective()
            Aproj = self.curve.affine_to_projective(self.A)

            self.assertEquals(NP, self.curve.add_points_projective(NP, NP))
            self.assertEquals(Aproj, self.curve.add_points_projective(Aproj, NP))
            self.assertEquals(Aproj, self.curve.add_points_projective(NP, Aproj))

    def test_projective_double_infinity(self):
        if self.HAS_INF:
            NP = self.curve.neutral_point_projective()

            self.assertEquals(NP, self.curve.double_point_projective(NP))

    def test_multiplicastion_projective(self):
        self.assertEquals(
            self.MUL_P_1,
            self.curve.projective_to_affine(
                montgomery_ladder_projective(self.MUL_K_1,
                                             self.curve.affine_to_projective(self.bp),
                                             self.curve)))

        self.assertEquals(
            self.MUL_P_2,
            self.curve.projective_to_affine(
                montgomery_ladder_projective(self.MUL_K_2,
                                             self.curve.affine_to_projective(self.bp),
                                             self.curve)))


class ShortWeierstrassTestCase(unittest.TestCase, CommonCurveTestsMixin, ProjectiveCoordinateTestsMixin):

    HAS_INF = True

    A = (28937482748732473272897498274273472742774274986, 33305269008585405502505469027798241419677945708730054157481301193203107088561)
    B = (9953545743011090700414932281601853911810693602092897893278312141468267489961, 114623072207054754832614539732676646402358038272928816598777008811037317832839)
    AplusB = (96207774072596727529939662469544277511796379399647366094983596356781685872159, 35300157377482363232860404691053863017929087870821103208612923014790370167467)
    Ax2 = (70247058299747858673597439551441565009625257406585803008177815317191957509437, 81738978117032266056298042554300547655878526001305737205290595047700968235290)
    negB = (9953545743011090700414932281601853911810693602092897893278312141468267489961, 1169017003301493930082907216730927127728105142361497596756622497829780021112)

    MUL_K_1 = 112233445566778899
    MUL_P_1 = (0x339150844EC15234807FE862A86BE77977DBFB3AE3D96F4C22795513AEAAB82F, 0xB1C14DDFDC8EC1B2583F51E85A5EB3A155840F2034730E9B5ADA38B674336A21)

    MUL_K_2 = 12078056106883488161242983286051341125085761470677906721917479268909056
    MUL_P_2 = (0x5E6C8524B6369530B12C62D31EC53E0288173BD662BDF680B53A41ECBCAD00CC, 0x447FE742C2BFEF4D0DB14B5B83A2682309B5618E0064A94804E9282179FE089F)

    def setUp(self):
        # Test with NIST P-256
        field = Field(2**256 - 2**224 + 2**192 + 2**96 - 1)
        nistp256 = ShortWeierstrass(-3, 41058363725152142129326129780047268409114441015993725554835256314039467401291, field)
        base_point = (48439561293906451759052585252797914202762949526041747995844080717082404635286, 36134250956749795798585127919587881956611106672985015071877198253568414405109)

        self.curve = nistp256
        self.bp = base_point

    def test_getting_y_from_x(self):
        self.assertTrue(self.A in self.curve.get_y(self.A[0]))
        self.assertTrue(self.B in self.curve.get_y(self.B[0]))
        self.assertTrue(self.bp in self.curve.get_y(self.bp[0]))
        self.assertTrue(self.AplusB in self.curve.get_y(self.AplusB[0]))
        self.assertTrue(self.negB in self.curve.get_y(self.negB[0]))


class MontgomeryTestCase(unittest.TestCase, CommonCurveTestsMixin):

    HAS_INF = True

    A = (4, 10396089888167458996693606908380331970145732977558722329349539962582616845133)
    B = (57896044618658097711785492504343953926634992332819468005417807693008429988855, 20648066745302263758022166077102042423099773856289430574108999690724270206752)
    AplusB = (5719695188011382591708688852426477362131995332637993518588075749885560482611, 56505842971816567066780380311011328716062813470368590554418668765449755842932)
    Ax2 = (7870538420911991717785453005997772929543321076076670267330433180192557165563, 51462988753647980434029505129423452788607920152547915666106126236317133170583)
    negB = (57896044618658097711785492504343953926634992332819468005417807693008429988855, 37247977873355833953763326427241911503535218476530851445619792313232294613197)

    MUL_K_1 = 112233445566778899
    MUL_P_1 = (16451190848088295144335504497878510182252812127695227532773102179055115380059, 20666130369112553010596845835900540409695299864160032674504769878919780324447)

    MUL_K_2 = 12078056106883488161242983286051341125085761470677906721917479268909056
    MUL_P_2 = (9148393841669501911815419162694955736881614650499055279038041633798855622223, 35637307743073598126576104765045054352535325500213513003691779802726441239262)

    def setUp(self):
        # Test with Curve25519
        field = Field(2**255 - 19)
        curve25519 = MontgomeryCurve(486662, 1, field)
        base_point = (9, 14781619447589544791020593568409986887264606134616475288964881837755586237401)

        self.curve = curve25519
        self.bp = base_point

    def test_getting_y_from_x(self):
        self.assertTrue(self.A in self.curve.get_y(self.A[0]))
        self.assertTrue(self.B in self.curve.get_y(self.B[0]))
        self.assertTrue(self.bp in self.curve.get_y(self.bp[0]))
        self.assertTrue(self.AplusB in self.curve.get_y(self.AplusB[0]))
        self.assertTrue(self.negB in self.curve.get_y(self.negB[0]))

    def test_convert_to_short_weierstrass(self):

        # Test with Curve41417
        field = Field(2**414 - 17)
        curve41417 = EdwardsCurve(1, 3617, Field(2**414 - 17))
        curve41417_bp = (17319886477121189177719202498822615443556957307604340815256226171904769976866975908866528699294134494857887698432266169206165, 34)

        # this is tested in the Montgomery test case.
        curve41417monty, P_to_monty, P_from_monty = curve41417.to_montgomery()
        curve41417monty_bp = P_to_monty(curve41417_bp)

        # now finally convert to short weierstrass

        weiss, P_to_weiss, P_from_weiss = curve41417monty.to_short_weierstrass()

        self.assertEquals(42307582002575910332922579714097346549017899709713998034217522897561970639123926132812109468141778230245837569601494931198756, weiss.a)
        self.assertEquals(42307582002575910332922579714097346549017899709713998034217522897561970639123926132812109468141778230245837569601494877203573, weiss.b)

        self.assertEquals((33333246426271929353211729471713060917408042195532240875444108949594279897491578165245904429445037393527023539686026309646457, 2236671449683305925398969480507433209994648385971289644656272082874689574321388075188206152980709096399807140440181156775230), P_to_weiss(curve41417monty_bp))

        self.assertEquals(curve41417monty_bp, P_from_monty(P_to_monty(curve41417monty_bp)))


class EdwardsTestCase(unittest.TestCase, CommonCurveTestsMixin, ProjectiveCoordinateTestsMixin):

    HAS_INF = False

    # XXX: Values below are not verified by other software :-(
    A = (8616666371206267167948241317493115735480654267599063779918300008662332373439067505541225678031087693668986087693131908520628L, 28717294693633539301394667122698466228242397902744113068564379516062313985774198446790896975083186638897505386461866494194440L)
    B = (3866197932632166713922409023601869511491251288212831964046182131914487387913335107084506690483883697530226479381807446621922L, 26433866805097075046906857010004219466513866826455325088205333045898955643952464816575071793571968012644610460296556980410477L)
    AplusB = (41959748609177754624304702165300526028840491867946322890204718103258643027885582018669075197576999770562138094742381437061577L, 25998714995907598410490070434672346441349914844128757423042349337515218298963538377495599926364640518547462920855944539817894L)
    Ax2 = (28141733563285035865793686612028897050466581446022626929212891093550718345570118317842351040995388904047761376400515052062121L, 24325817562159635675663633436486290626470417346693872419538680100493874655911110496012324792374554103850437663025490721982433L)
    negB = (38441384069943743619000170690495477037526648421501166070171340765647483251210591025727602777657894532715611090219687484850445L, 26433866805097075046906857010004219466513866826455325088205333045898955643952464816575071793571968012644610460296556980410477L)

    MUL_K_1 = 112233445566778899
    MUL_P_1 = (30546484635907854868331108563723484987364563607591941811892627170882891004603474350951906710441804919375906557238147264372440L, 12121435438090892414887576633047222532945889037312450028928210690628632178949997868388861932641009914216012453765524337157455L)

    MUL_K_2 = 12078056106883488161242983286051341125085761470677906721917479268909056
    MUL_P_2 = (11913214868765532789914127048695588278116657635417155935063797132492289253105828807812586386883536561252775748248785166325287L, 35878585899420598813414783256533947679488146167016243811103795390234543226486781458473617335264824679658889013620092532804237L)


    def setUp(self):
        # Test with Curve41417
        field = Field(2**414 - 17)
        ed41417 = EdwardsCurve(1, 3617, field)

        self.curve = ed41417
        self.bp = (17319886477121189177719202498822615443556957307604340815256226171904769976866975908866528699294134494857887698432266169206165, 34)

    def test_getting_x_from_y(self):
        self.assertTrue(self.A in self.curve.get_x(self.A[1]))
        self.assertTrue(self.B in self.curve.get_x(self.B[1]))
        self.assertTrue(self.bp in self.curve.get_x(self.bp[1]))
        self.assertTrue(self.AplusB in self.curve.get_x(self.AplusB[1]))
        self.assertTrue(self.negB in self.curve.get_x(self.negB[1]))

    # This works for Twisted Edwards curves.
    def test_addition_A_plus_A_equals_doubling_A(self):
        self.assertEquals(self.Ax2, self.curve.add_points(self.A, self.A))

    def test_shitty_test_data(self):
        raise Exception('data not independently verified for Edwards Curve test case')

    def test_convert_to_montgomery(self):
        monty, P_to_monty, P_from_monty = self.curve.to_montgomery()

        self.assertEquals(16426948321796620051831665353593106901222657962510634192489325815314437714969577513956914185086022299575540914745713186888052, monty.a)
        self.assertEquals(16426948321796620051831665353593106901222657962510634192489325815314437714969577513956914185086022299575540914745713186888054, monty.b)

        self.assertEquals((39743486123631915767290908216273264939986511848519210274567976055285487570086112427793193742799852276897604989625646753807374, 839933412164472433702663125412881421097707462819558268773516747868629183550784604331227615346870906026576625124321601338194), P_to_monty(self.bp))

        self.assertEquals(self.bp, P_from_monty(P_to_monty(self.bp)))


class TwistedEdwardsTestCase(unittest.TestCase, CommonCurveTestsMixin, ProjectiveCoordinateTestsMixin):

    HAS_INF = False

    A = (27481316271530520064648624528946075020604099226833435014658659335205728969530L, 49183306314203018186757512478661807730540880701773633805641219564336674550969L)
    B = (15112221349535400772501151409588531511454012693041857206046113283949847762202L, 46316835694926478169428394003475163141307993866256225615783033603165251855960L)
    AplusB = (46654725727887309172946098228562394131542193577392406590236117120721125965966L, 9874863605069078903873662809862038509278995146436578859837106983843358600506L)
    Ax2 = (43920005206699697475173593044401900729295086664698779414933667463935700550876L, 35870488498917683536087484065659952248796089902966194562695147652774440091107L)
    negB = (42783823269122696939284341094755422415180979639778424813682678720006717057747, 46316835694926478169428394003475163141307993866256225615783033603165251855960L)

    MUL_K_1 = 112233445566778899
    MUL_P_1 = (31600853386398476776061775690061493014435707717063663537080063585342091008114L, 49971842736542153624717355285388443191803756171759862390024275941521523321905L)

    MUL_K_2 = 12078056106883488161242983286051341125085761470677906721917479268909056
    MUL_P_2 = (53307823263028338661792150995493581614124080123163921964878358867746246316544L, 46690031596131423240019242885040885044892847324133512893321009649759777980104L)

    def setUp(self):
        # Test with Ed25519
        field = Field(2**255 - 19)
        ed25519 = TwistedEdwardsCurve(-1, field.div(-121665, 121666), field)

        base_point = (15112221349535400772501151409588531511454012693041857206046113283949847762202L,
                      46316835694926478169428394003475163141307993866256225615783033603165251855960L)

        self.curve = ed25519
        self.bp = base_point

    def test_getting_x_from_y(self):
        self.assertTrue(self.A in self.curve.get_x(self.A[1]))
        self.assertTrue(self.B in self.curve.get_x(self.B[1]))
        self.assertTrue(self.bp in self.curve.get_x(self.bp[1]))
        self.assertTrue(self.AplusB in self.curve.get_x(self.AplusB[1]))
        self.assertTrue(self.negB in self.curve.get_x(self.negB[1]))

    # This works for Twisted Edwards curves.
    def test_addition_A_plus_A_equals_doubling_A(self):
        self.assertEquals(self.Ax2, self.curve.add_points(self.A, self.A))

    def test_montgomery_mapping(self):
        monty, map_func_to, map_func_from = self.curve.to_montgomery()

        #print map_func_to((3, 1))
        #print map_func_from(monty.neutral_point())

        self.assertEquals(
            self.Ax2,
            map_func_from(monty.double_point(
                map_func_to(self.A))))

        self.assertEquals(
            self.A,
            map_func_from(monty.add_points(
                None,
                map_func_to(self.A))))

        self.assertEquals(
            None,
            map_func_from(monty.add_points(
                None,
                None)))


if __name__ == '__main__':
    unittest.main()
