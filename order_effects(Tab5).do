/*
This script performs some additional analyses reported in the paper:
- A test of order effects reported in Table 5 (* for p<0.1 and ** for p<0.05)
- A test of consequentialism
*/

***********************************
***********************************
*          ORDER EFFECTS          *
***********************************
***********************************

import delimited cleaned_data.csv, clear
drop if ce_w4 == 1

*********************************
* CALCULATE AMB ATT PROPORTIONS *
*********************************

gen prop_averse = amb_attitude == "averse"
gen prop_neutral = amb_attitude == "neutral"
gen prop_seeking = amb_attitude == "seeking"

prtest prop_averse, by(order_treatment)
prtest prop_neutral, by(order_treatment)
prtest prop_seeking, by(order_treatment)


*****************************
* RISKY STATE, INFO PREMIUM *
*****************************
* Testing whether Prop(Information Premia =~ 0) differ between orders A and B
gen pr_approx = abs(diffpr) <= 1
prtest pr_approx, by(order_treatment) // across all
by amb_attitude, sort : prtest pr_approx, by(order_treatment) // within amb attitudes

* Testing whether Prop(Information Premia = 0) differ between orders A and B
gen pr_equal = diffpr == 0
prtest pr_equal, by(order_treatment) // across all
by amb_attitude, sort : prtest pr_equal, by(order_treatment) // within amb attitudes

* Testing whether Prop(Information Premia > 0) differ between orders A and B
gen pr_positive = diffpr > 0
prtest pr_positive, by(order_treatment) // across all
by amb_attitude, sort : prtest pr_positive, by(order_treatment) // within amb attitudes

* Testing whether Prop(Information Premia < 0) differ between orders A and B
gen pr_negative = diffpr < 0
prtest pr_negative, by(order_treatment) // across all
by amb_attitude, sort : prtest pr_negative, by(order_treatment) // within amb attitudes

******************************
* RISKY STATE, VALUE OF INFO *
******************************

* Testing whether Prop(Value of Info =~ 0) differ between orders A and B
gen vr_approx = abs(diffvr) <= 1
prtest vr_approx, by(order_treatment) // across all
by amb_attitude, sort : prtest vr_approx, by(order_treatment) // within amb attitudes

* Testing whether Prop(Value of Info = 0) differ between orders A and B
gen vr_equal = diffvr == 0
prtest vr_equal, by(order_treatment) // across all
by amb_attitude, sort : prtest vr_equal, by(order_treatment) // within amb attitudes

* Testing whether Prop(Value of Info > 0) differ between orders A and B
gen vr_positive = diffvr > 0
prtest vr_positive, by(order_treatment) // across all
by amb_attitude, sort : prtest vr_positive, by(order_treatment) // within amb attitudes

* Testing whether Prop(Value of Info < 0) differ between orders A and B
gen vr_negative = diffvr < 0
prtest vr_negative, by(order_treatment) // across all
by amb_attitude, sort : prtest vr_negative, by(order_treatment) // within amb attitudes

*****************************
* AMBIG STATE, INFO PREMIUM *
*****************************
* Testing whether Prop(Information Premia =~ 0) differ between orders A and B
gen pa_approx = abs(diffpa) <= 1
prtest pa_approx, by(order_treatment) // across all
by amb_attitude, sort : prtest pa_approx, by(order_treatment) // within amb attitudes

* Testing whether Prop(Information Premia = 0) differ between orders A and B
gen pa_equal = diffpa == 0
prtest pa_equal, by(order_treatment) // across all
by amb_attitude, sort : prtest pa_equal, by(order_treatment) // within amb attitudes

* Testing whether Prop(Information Premia > 0) differ between orders A and B
gen pa_positive = diffpa > 0
prtest pa_positive, by(order_treatment) // across all
by amb_attitude, sort : prtest pa_positive, by(order_treatment) // within amb attitudes

* Testing whether Prop(Information Premia < 0) differ between orders A and B
gen pa_negative = diffpa < 0
prtest pa_negative, by(order_treatment) // across all
by amb_attitude, sort : prtest pa_negative, by(order_treatment) // within amb attitudes

******************************
* AMBIG STATE, VALUE OF INFO *
******************************

* Testing whether Prop(Value of Info =~ 0) differ between orders A and B
gen va_approx = abs(diffva) <= 1
prtest va_approx, by(order_treatment) // across all
by amb_attitude, sort : prtest va_approx, by(order_treatment) // within amb attitudes

* Testing whether Prop(Value of Info = 0) differ between orders A and B
gen va_equal = diffva == 0
prtest va_equal, by(order_treatment) // across all
by amb_attitude, sort : prtest va_equal, by(order_treatment) // within amb attitudes

* Testing whether Prop(Value of Info > 0) differ between orders A and B
gen va_positive = diffva > 0
prtest va_positive, by(order_treatment) // across all
by amb_attitude, sort : prtest va_positive, by(order_treatment) // within amb attitudes

* Testing whether Prop(Value of Info < 0) differ between orders A and B
gen va_negative = diffva < 0
prtest va_negative, by(order_treatment) // across all
by amb_attitude, sort : prtest va_negative, by(order_treatment) // within amb attitudes


************************
* CONSEQUENTIALIM TEST *
************************

gen conseq13index = ce_index1 - ce_index3
tab conseq13index if chose_info3 == 0

gen conseq23index = ce_index2 - ce_index3
tab conseq23index if chose_info3 == 1

gen conseq46index = ce_index4 - ce_index6
tab conseq46index if chose_info6 == 0

gen conseq56index = ce_index5 - ce_index6
tab conseq56index if chose_info6 == 1