// import type { PageServerLoad } from "./$types";
// import { getCookies } from "$lib/utils/cookies";
// import { redirect, error } from '@sveltejs/kit';
// import { fetchAcount, fetchQuiz, fetchQuizAnswer } from "$lib/utils/api/server-apis";
//
//
// export const load: PageServerLoad = async ({ cookies, fetch, url }) => {
//     let token = getCookies("auth_token");
//     if (!token) {
//         throw redirect(302, `/Login?redirect=${encodeURIComponent(url.pathname)}`);
//     }
//     const [account, valuTest, acuTestPic, acuTestText] = await Promise.all([
//         fetchAcount(fetch, token),
//         fetchQuiz(fetch, token, 'ValuTest'),
//         fetchQuiz(fetch, token, 'AcuTest_pic'),
//         fetchQuiz(fetch, token, 'AcuTest_text')]);
//
//     function minutesSince(dateString: string) {
//         const now = new Date();
//         const qdate = new Date(dateString);
//         return Math.floor((now.valueOf() - qdate.valueOf()) / 1000 / 60);
//     }
//
//     const notStartedValPic = valuTest?.quiz_time === 'not_started';
//     const isValuDone = valuTest?.quiz_time && !notStartedValPic ? minutesSince(valuTest.quiz_time) >= 10 : false;
//
//     const notStartedAcuText = acuTestText?.quiz_time === 'not_started';
//     const isAcuTextDone = acuTestText?.quiz_time && !notStartedAcuText ? minutesSince(acuTestText.quiz_time) >= 6 : false;
//
//     const notStartedAcuPic = acuTestPic?.quiz_time === 'not_started';
//     const isAcuPicDone = acuTestPic?.quiz_time && !notStartedAcuPic ? minutesSince(acuTestPic.quiz_time) >= 5 : false;
//
//     return {
//         first_name: account.first_name ?? '',
//         last_name: account.last_name ?? '',
//         hasValPerm: !!account.valTest_permition,
//         hasAcuPerm: !!account.acuTest_permition,
//         isValuDone,
//         isAcuTextDone,
//         isAcuPicDone,
//         notStartedValPic,
//         notStartedAcuText,
//         notStartedAcuPic,
//     };
//
// }
