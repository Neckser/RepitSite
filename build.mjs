import fs from 'fs';
import path from 'path';
import esbuild from 'esbuild';

const entries = [
  {
    html: 'src/app/templates/auth/login/login.html',
    css: 'src/app/templates/auth/login/login.css',
    out: 'build/auth/login.html',
  },
  {
    html: 'src/app/templates/auth/loginrepfailed/loginrepfailed.html',
    css: 'src/app/templates/auth/loginrepfailed/loginrepfailed.css',
    out: 'build/auth/loginrepfailed.html',
  },
  {
    html: 'src/app/templates/auth/loginstudfailed/loginstudfailed.html',
    css: 'src/app/templates/auth/loginstudfailed/loginstudfailed.css',
    out: 'build/auth/loginstudfailed.html',
  },
  {
    html: 'src/app/templates/register/regstud/regstud.html',
    css: 'src/app/templates/register/regstud/regstud.css',
    out: 'build/register/regstud.html',
  },
  {
    html: 'src/app/templates/register/regtut/regtut.html',
    css: 'src/app/templates/register/regtut/regtut.css',
    out: 'build/register/regtut.html',
  },
  {
    html: 'src/app/templates/mainpages/mainpage/mainpage.html',
    css: 'src/app/templates/mainpages/mainpage/mainpage.css',
    js: 'src/app/templates/mainpages/mainpage/mainpage.js',
    out: 'build/mainpages/mainpage.html',
  },
  {
    html: 'src/app/templates/mainpages/hometut/hometut.html',
    css: 'src/app/templates/mainpages/hometut/hometut.css',
    out: 'build/mainpages/hometut.html',
  },
  {
    html: 'src/app/templates/findtut/tutlist/tutlist.html',
    css: 'src/app/templates/findtut/tutlist/tutlist.css',
    out: 'build/findtut/tutlist.html',
  },
  {
    html: 'src/app/templates/findtut/findtut/findtut.html',
    css: 'src/app/templates/findtut/findtut/findtut.css',
    out: 'build/findtut/findtut.html',
  },
  {
    html: 'src/app/templates/findtut/findtutidfailed/findtutidfailed.html',
    css: 'src/app/templates/findtut/findtutidfailed/findtutidfailed.css',
    out: 'build/findtut/findtutidfailed.html',
  },
  {
    html: 'src/app/templates/profiles/studprofile/studprofile.html',
    css: 'src/app/templates/profiles/studprofile/studprofile.css',
    out: 'build/profiles/studprofile.html',
  },
  {
    html: 'src/app/templates/profiles/profiletut/profiletut.html',
    css: 'src/app/templates/profiles/profiletut/profiletut.css',
    out: 'build/profiles/profiletut.html',
  },
  {
    html: 'src/app/templates/profiles/edittutprofile/edittutprofile.html',
    css: 'src/app/templates/profiles/edittutprofile/edittutprofile.css',
    js: 'src/app/templates/profiles/edittutprofile/edittutprofile.js',
    out: 'build/profiles/edittutprofile.html',
  },
  {
    html: 'src/app/templates/profiles/editstudprofile/editstudprofile.html',
    css: 'src/app/templates/profiles/editstudprofile/editstudprofile.css',
    js: 'src/app/templates/profiles/editstudprofile/editstudprofile.js',
    out: 'build/profiles/editstudprofile.html',
  },
  {
    html: 'src/app/templates/homeworks/homeworkstut/homeworkstut.html',
    css: 'src/app/templates/homeworks/homeworkstut/homeworkstut.css',
    out: 'build/homeworks/homeworkstut.html',
  },
  {
    html: 'src/app/templates/timetable/studtime/studtime.html',
    css: 'src/app/templates/timetable/studtime/studtime.css',
    out: 'build/timetable/studtime.html',
  },
  {
    html: 'src/app/templates/timetable/tuttime/tuttime.html',
    css: 'src/app/templates/timetable/tuttime/tuttime.css',
    out: 'build/timetable/tuttime.html',
  },
  {
    html: 'src/app/templates/grades/studgrades/studgrades.html',
    css: 'src/app/templates/grades/studgrades/studgrades.css',
    out: 'build/grades/studgrades.html',
  },
  {
    html: 'src/app/templates/grades/tutgrades/tutgrades.html',
    css: 'src/app/templates/grades/tutgrades/tutgrades.css',
    out: 'build/grades/tutgrades.html',
  },
  {
    html: 'src/app/templates/errors/error/error.html',
    css: 'src/app/templates/errors/error/error.css',
    out: 'build/errors/error.html',
  },
  {
    html: 'src/app/templates/ctests/tutctest/tutctest.html',
    css: 'src/app/templates/ctests/tutctest/tutctest.css',
    js: 'src/app/templates/ctests/tutctest/tutctest.js',
    out: 'build/ctests/tutctest.html',
  },
  {
    html: 'src/app/templates/ctests/tuttests/tuttests.html',
    css: 'src/app/templates/ctests/tuttests/tuttests.css',
    out: 'build/ctests/tuttests.html',
  },
  {
    html: "src/app/templates/landing/mainlanding/mainlanding.html",
    css: "src/app/templates/landing/mainlanding/mainlanding.css",
    out: "build/landing/mainlanding.html",
  },
  {
    html: "src/app/templates/landing/policy/policy.html",
    css: "src/app/templates/landing/policy/policy.css",
    js: "src/app/templates/landing/policy/policy.js",
    out: "build/landing/policy.html",
  },
  {
    html: "src/app/templates/landing/cookies/cookies.html",
    css: "src/app/templates/landing/cookies/cookies.css",
    js: "src/app/templates/landing/cookies/cookies.js",
    out: "build/landing/cookies.html",
  },
  {
    html: "src/app/templates/landing/terms/terms.html",
    css: "src/app/templates/landing/terms/terms.css",
    out: "build/landing/terms.html",
  },
  {
    html: "src/app/templates/landing/contact/contact.html",
    css: "src/app/templates/landing/contact/contact.css",
    out: "build/landing/contact.html",
  },
  {
    html: "src/app/templates/landing/faq/faq.html",
    css: "src/app/templates/landing/faq/faq.css",
    out: "build/landing/faq.html",
  },
  {
    html: 'src/app/templates/cards/hwcard.html',
    out: 'build/cards/hwcard.html',
  },
  {
    html: 'src/app/templates/cards/studcard.html',
    out: 'build/cards/studcard.html',
  },
  {
    html: 'src/app/templates/cards/tutcards.html',
    out: 'build/cards/tutcards.html',
  },
  {
    html: 'src/app/templates/cards/hwtutcard.html',
    out: 'build/cards/hwtutcard.html',
  },
  {
    html: 'src/app/templates/cards/lesson.html',
    out: 'build/cards/lesson.html',
  },
  {
    html: 'src/app/templates/cards/nolessons.html',
    out: 'build/cards/nolessons.html',
  },
  {
    html: 'src/app/templates/cards/tutlesson.html',
    out: 'build/cards/tutlesson.html',
  },
  {
    html: 'src/app/templates/cards/gradestr.html',
    out: 'build/cards/gradestr.html',
  },
  {
    html: 'src/app/templates/cards/gradestemplate.html',
    out: 'build/cards/gradestemplate.html',
  },
  {
    html: 'src/app/templates/cards/tuttest.html',
    out: 'build/cards/tuttest.html',
  },
];

for (const entry of entries) {
  let html = fs.readFileSync(entry.html, 'utf8');
  let css = fs.existsSync(entry.css) ? fs.readFileSync(entry.css, 'utf8') : '';
  let js = '';
  if (fs.existsSync(entry.js)) {
    const result = await esbuild.build({
      entryPoints: [entry.js],
      bundle: true,
      minify: true,
      write: false,
      format: 'iife',
    });
    js = result.outputFiles[0].text;
  }
  html = html.replace('</head>', `<style>${css}</style></head>`);
  html = html.replace('</body>', `<script>${js}</script></body>`);

  const outDir = path.dirname(entry.out);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(entry.out, html, 'utf8');
  console.log(`Built ${entry.out}`);
}

