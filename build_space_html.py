# -*- coding: utf-8 -*-
"""
Build python-space.html — the downloadable, single-file, light "space edition"
of the Python tutorial.

Data source (read-only): ~/workspace/github-io-site/gen_site.py
  - L (41 lessons), CODING (hands-on tasks), STAGES, DIFF, MEALS_CSV, LEDGER_CSV

De-personalisation (hard requirement — this file is for public download):
  - Course content that used the author's own name as an example ("Hobart" in
    lesson 7's input example and its coding task) is rewritten to the generic
    example name 「小明」.
  - Branding is generic ("Python 自学教程"); no author name, no personal
    links, fresh localStorage keys that start empty for every downloader.
  - After generation we assert that none of the forbidden identifiers appear
    anywhere in the output file.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.expanduser("~/workspace/github-io-site/gen_site.py")
OUT = os.path.join(HERE, "python-space.html")

FORBIDDEN = ["Hobart", "HOBART", "hobart", "Samuel", "SZE", "hobartsze"]
GENERIC_NAME = "小明"


def load_source():
    spec = importlib.util.spec_from_file_location("gen_site_src", SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sanitize(obj):
    """Recursively replace the author's name in course strings with a generic one."""
    if isinstance(obj, str):
        return obj.replace("Hobart", GENERIC_NAME)
    if isinstance(obj, list):
        return [sanitize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    return obj


def build_data(mod):
    data = []
    for i, l in enumerate(mod.L):
        d = dict(l)
        d["gi"] = i
        d["diff"] = mod.DIFF[i]
        d["explain"] = mod.EXPLAIN[i]
        if i in mod.CODING:
            d["coding"] = mod.CODING[i]
        data.append(d)
    return sanitize(data)


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Python 自学教程 · 空间版（下载版）</title>
<meta name="description" content="41 课 Python 自学路线：从 print 到 pandas 账本报告、Excel、数据清洗与网络爬虫。每课都有代码演示、选择题和可即时判定的动手编程题。单文件下载版，双击即可打开。">
<style>
:root{
  --bg:#f3edde; --paper:#fbf7ec; --card:#fffdf6;
  --ink:#221b0f; --ink2:#4c4333; --muted:#7e7360; --muted2:#a5947a;
  --line:rgba(84,66,28,.16); --line2:rgba(84,66,28,.3);
  --gold:#a97b14; --gold2:#c1901f; --gold-soft:rgba(169,123,20,.09);
  --green:#2e7d46; --red:#bc4430; --teal:#1e7a6c;
  --serif:"Noto Serif SC","Songti SC","STSong",Georgia,"Times New Roman",serif;
  --sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans SC","Microsoft YaHei","Segoe UI",sans-serif;
  --grot:"Avenir Next","Trebuchet MS",var(--sans);
  --mono:"JetBrains Mono","SF Mono",Menlo,Consolas,"Courier New",monospace;
  --ease:cubic-bezier(.22,1,.36,1);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased;overflow-x:hidden;
  background-image:radial-gradient(1100px 600px at 85% -5%,rgba(193,144,31,.1),transparent 60%),radial-gradient(900px 700px at -10% 30%,rgba(169,123,20,.06),transparent 55%)}
::selection{background:rgba(169,123,20,.28)}
a{color:inherit}
button{font-family:var(--sans)}
/* ---------- glass ---------- */
.glass{background:rgba(255,252,243,.62);backdrop-filter:blur(18px) saturate(1.45);-webkit-backdrop-filter:blur(18px) saturate(1.45);
  border:1px solid rgba(255,255,255,.7);box-shadow:inset 0 1px 0 rgba(255,255,255,.85),inset 0 -1px 0 rgba(169,123,20,.08),0 20px 44px rgba(96,74,18,.14)}
/* ---------- nav ---------- */
nav{position:sticky;top:0;z-index:50;background:rgba(251,247,236,.72);backdrop-filter:blur(18px) saturate(1.45);-webkit-backdrop-filter:blur(18px) saturate(1.45);
  border-bottom:1px solid var(--line);box-shadow:inset 0 1px 0 rgba(255,255,255,.8),0 10px 30px rgba(96,74,18,.07)}
.nav-in{max-width:1060px;margin:0 auto;padding:13px 24px;display:flex;align-items:center;gap:16px}
.logo{font-family:var(--grot);font-weight:700;letter-spacing:.16em;font-size:13px;cursor:pointer}
.logo b{color:var(--gold)}
.nav-in .sp{flex:1}
.navlink{font-size:13.5px;color:var(--ink2);background:none;border:none;cursor:pointer;padding:8px 6px}
.navlink:hover{color:var(--gold)}
.ringwrap{display:flex;align-items:center;gap:10px;font-size:12.5px;color:var(--muted)}
.xp{font-family:var(--grot);font-weight:700;font-size:13px;color:var(--gold);letter-spacing:.05em}
/* ---------- views & transitions ---------- */
.view{display:none}
.view.active{display:block;animation:viewIn .38s var(--ease)}
@keyframes viewIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.wrap{max-width:1060px;margin:0 auto;padding:0 24px}
/* ---------- masthead & hero ---------- */
.masthead{display:flex;justify-content:space-between;align-items:baseline;gap:18px;border-bottom:1px solid var(--line2);
  padding:34px 0 13px;font-family:var(--grot);font-size:11.5px;letter-spacing:.22em;color:var(--muted);white-space:nowrap;overflow:hidden}
.hero{position:relative;padding:52px 0 10px;overflow:hidden}
.ghost{position:absolute;right:-30px;top:-38px;font-family:var(--serif);font-weight:900;font-size:clamp(150px,26vw,300px);
  line-height:1;color:rgba(169,123,20,.07);pointer-events:none;user-select:none}
.kicker{font-family:var(--grot);font-size:12px;letter-spacing:.34em;color:var(--gold);display:flex;align-items:center;gap:12px;text-transform:uppercase}
.kicker::before{content:"";width:34px;height:1px;background:var(--gold)}
h1{font-family:var(--serif);font-weight:900;font-size:clamp(42px,6.6vw,76px);line-height:1.16;margin:20px 0 6px;letter-spacing:0}
h1 .accent{color:var(--gold)}
.hero p.sub{color:var(--ink2);font-size:clamp(15px,1.8vw,17.5px);line-height:1.95;max-width:60ch;margin-top:14px}
.cta{display:flex;gap:14px;margin-top:32px;flex-wrap:wrap}
.btn{font-weight:700;font-size:15px;border-radius:999px;padding:13px 29px;cursor:pointer;border:1px solid transparent;transition:transform .18s ease,box-shadow .18s ease,background .18s}
.btn:active{transform:scale(.97)}
.btn-gold{background:linear-gradient(120deg,var(--gold2),var(--gold));color:#fff8e6;box-shadow:0 10px 30px rgba(169,123,20,.3)}
.btn-gold:hover{transform:translateY(-2px);box-shadow:0 15px 38px rgba(169,123,20,.38)}
.btn-ghost{background:rgba(255,252,243,.5);color:var(--ink);border-color:var(--line2)}
.btn-ghost:hover{background:#fffdf6;transform:translateY(-2px)}
.btn:disabled{opacity:.5;cursor:default;transform:none}
.stats{display:flex;gap:clamp(22px,5vw,54px);margin-top:46px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:24px}
.stat .n{font-family:var(--serif);font-size:clamp(29px,3.8vw,42px);font-weight:900}
.stat .n em{font-style:normal;color:var(--gold);font-size:.55em;font-weight:700}
.stat .t{color:var(--muted);font-size:12px;letter-spacing:.18em;margin-top:4px}
.progress-card{margin-top:34px;border-radius:18px;padding:22px 26px;display:flex;gap:26px;align-items:center;flex-wrap:wrap}
.progress-card .pc-t{font-family:var(--grot);font-size:11px;letter-spacing:.26em;color:var(--muted)}
.progress-card .pc-n{font-family:var(--serif);font-size:30px;font-weight:900;margin-top:4px}
.progress-card .pc-bar{flex:1;min-width:180px;height:6px;border-radius:99px;background:rgba(84,66,28,.14);overflow:hidden}
.progress-card .pc-bar i{display:block;height:100%;background:linear-gradient(90deg,var(--gold),var(--gold2));border-radius:99px;transition:width .8s var(--ease)}
/* hero IDE */
.ide{margin-top:44px;position:relative;border-radius:16px;background:#171208;border:1px solid rgba(84,66,28,.4);box-shadow:0 36px 80px rgba(80,60,10,.28);overflow:hidden}
.ide-bar{display:flex;align-items:center;gap:8px;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,.09);background:rgba(255,255,255,.03)}
.dot{width:12px;height:12px;border-radius:50%;flex:none}
.ide-tab{margin-left:10px;font-family:var(--mono);font-size:12.5px;color:#e8dfc8;background:rgba(255,255,255,.07);padding:5px 14px;border-radius:8px}
.ide-body{display:grid;grid-template-columns:1fr 290px;min-height:230px}
.ide-code{padding:20px 22px;font-family:var(--mono);font-size:14.5px;line-height:1.85;white-space:pre-wrap;word-break:break-all;color:#f0e9d6}
.ide-console{border-left:1px solid rgba(255,255,255,.09);background:rgba(0,0,0,.3);padding:18px;font-family:var(--mono);font-size:13px;line-height:1.9;color:#b9f0cf}
.ide-console .hd{color:#9a8c66;font-size:11px;letter-spacing:.22em;margin-bottom:8px}
.caret{display:inline-block;width:9px;height:18px;background:var(--gold2);vertical-align:-3px;animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.tok-kw{color:#d3a6f0}.tok-str{color:#b5d98c}.tok-num{color:#ffb37a}.tok-fn{color:#93b8f5}.tok-cm{color:#8a7f63}
/* ---------- route ---------- */
.route{padding:56px 0 30px}
.route-head h2{font-family:var(--serif);font-weight:900;font-size:clamp(29px,4.2vw,44px)}
.route-head p{color:var(--ink2);line-height:1.85;margin-top:8px;max-width:68ch}
.search{margin:22px 0 4px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--line2);padding:11px 2px;max-width:440px}
.search input{background:none;border:none;outline:none;color:var(--ink);font-size:15px;width:100%;font-family:var(--sans)}
.search input::placeholder{color:var(--muted2)}
.achv{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 2px}
.bdg{font-size:12.5px;padding:7px 13px;border-radius:3px;border:1px solid var(--line);color:var(--muted);background:rgba(255,252,243,.45)}
.bdg.on{color:#fff8e6;font-weight:700;background:linear-gradient(120deg,var(--gold2),var(--gold));border-color:transparent;box-shadow:0 8px 20px rgba(169,123,20,.3)}
.stage{margin-top:54px}
.stage-head{display:flex;align-items:center;gap:16px;margin-bottom:10px;flex-wrap:wrap}
.plate{font-family:var(--grot);font-size:11px;letter-spacing:.24em;color:var(--gold);border:1px solid rgba(169,123,20,.5);padding:6px 12px;border-radius:3px}
.stage-head h3{font-family:var(--serif);font-size:24px;font-weight:900}
.stage-head .ss{color:var(--muted);font-size:13.5px;width:100%;margin-top:2px}
.stage-bar{flex:1;max-width:280px;height:5px;border-radius:99px;background:rgba(84,66,28,.13);overflow:hidden;margin-left:auto}
.stage-bar i{display:block;height:100%;background:linear-gradient(90deg,var(--gold),var(--gold2));transition:width .8s var(--ease)}
.stage-pct{font-family:var(--grot);font-size:13px;color:var(--muted);min-width:42px;text-align:right}
.lrows{border-bottom:1px solid var(--line)}
.lrow{position:relative;display:flex;gap:clamp(14px,3vw,26px);align-items:baseline;padding:21px 8px 22px;border-top:1px solid var(--line);cursor:pointer;transition:background .2s}
.lrow:hover{background:rgba(169,123,20,.055)}
.lrow .no{font-family:var(--serif);font-weight:900;font-size:clamp(27px,3.4vw,36px);color:var(--gold);min-width:58px;line-height:1;transform:translateY(3px)}
.lrow.done .no{color:var(--gold)}
.lrow .main{flex:1;min-width:0}
.lrow h4{font-family:var(--serif);font-size:18.5px;font-weight:900;line-height:1.45}
.lrow p{color:var(--muted);font-size:13.5px;line-height:1.7;margin-top:5px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.lrow .side{text-align:right;flex:none}
.lrow .meta{font-family:var(--mono);font-size:11.5px;color:var(--muted);white-space:nowrap}
.status{font-size:11px;letter-spacing:.1em;padding:4px 11px;border-radius:99px;border:1px solid var(--line2);color:var(--muted);display:inline-block;margin-top:7px}
.status.done{color:#fff8e6;background:linear-gradient(120deg,var(--gold2),var(--gold));border-color:transparent;font-weight:700}
.status.cur{color:var(--gold);border-color:rgba(169,123,20,.55);font-weight:700}
.diff{display:inline-flex;gap:3px;vertical-align:middle;margin-left:6px}
.diff i{display:block;width:14px;height:3px;background:rgba(84,66,28,.18)}
.diff i.on{background:var(--gold)}
.flag{display:flex;align-items:center;gap:10px;color:var(--muted2);font-size:12.5px;margin:14px 0 0 2px}
.flag::before{content:"⚑";color:var(--gold)}
.empty{display:none;color:var(--muted);padding:26px 4px}
/* ---------- lesson ---------- */
.backbtn{background:none;border:none;color:var(--muted);font-size:14px;cursor:pointer;padding:26px 0 0}
.backbtn:hover{color:var(--gold)}
.lesson-head{position:relative;padding:18px 0 4px;overflow:hidden}
.lesson-head .ghost{font-size:clamp(120px,20vw,220px);top:-24px}
.stg{font-family:var(--grot);font-size:11px;letter-spacing:.26em;color:var(--gold)}
.lesson-head h3{font-family:var(--serif);font-weight:900;font-size:clamp(25px,3.8vw,36px);line-height:1.35;margin-top:8px;max-width:22ch}
.sec-t{font-family:var(--grot);font-size:11.5px;letter-spacing:.28em;color:var(--muted);margin:32px 0 12px;display:flex;align-items:center;gap:10px}
.sec-t::after{content:"";flex:1;height:1px;background:var(--line)}
.intro{font-size:15.5px;line-height:1.95;color:var(--ink2)}
.intro p{margin:0 0 12px}
.intro p:last-child{margin-bottom:0}
.intro code{font-family:var(--mono);font-size:13.5px;background:rgba(84,66,28,.08);border:1px solid rgba(84,66,28,.18);border-radius:6px;padding:1px 6px}
.tip{margin-top:14px;border-left:3px solid var(--gold);background:var(--gold-soft);padding:13px 18px;border-radius:0 12px 12px 0;font-size:14.5px;line-height:1.8;color:#5c4a17}
.tip b{color:var(--gold)}
.demo-plate{border-radius:20px;padding:16px}
.codebox{border-radius:14px;background:#171208;border:1px solid rgba(84,66,28,.4);overflow:hidden}
.codebox .cb-bar{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid rgba(255,255,255,.09);background:rgba(255,255,255,.03)}
.codebox .fn{font-family:var(--mono);font-size:12px;color:#b3a888;margin-left:8px}
.runbtn{margin-left:auto;font-family:var(--sans);font-weight:700;font-size:12.5px;background:linear-gradient(120deg,var(--gold2),var(--gold));color:#fff8e6;border:none;border-radius:99px;padding:7px 18px;cursor:pointer}
.runbtn:disabled{opacity:.55;cursor:default}
.codebox pre{padding:18px 20px;font-family:var(--mono);font-size:14px;line-height:1.85;overflow-x:auto;min-height:60px;color:#f0e9d6}
.console{border-top:1px dashed rgba(255,255,255,.16);padding:0 20px;font-family:var(--mono);font-size:13.5px;line-height:1.9;color:#b9f0cf;opacity:0;max-height:0;overflow:hidden;transform:translateY(6px);transition:opacity .55s var(--ease),max-height .55s var(--ease),padding .55s var(--ease),transform .55s var(--ease)}
.console.show{opacity:1;max-height:340px;padding:14px 20px;transform:none}
.console .hd{color:#9a8c66;font-size:10.5px;letter-spacing:.24em;margin-bottom:4px}
/* quiz */
.qdots{display:flex;gap:8px;margin-bottom:16px}
.qdots i{width:26px;height:5px;border-radius:99px;background:rgba(84,66,28,.16);transition:background .3s}
.qdots i.ok{background:var(--green)}.qdots i.bad{background:var(--red)}.qdots i.now{background:var(--gold)}
.quiz-q{font-size:16.5px;font-weight:700;line-height:1.7}
.opts{margin-top:16px;display:grid;gap:11px}
.opt{text-align:left;font-family:var(--sans);font-size:15px;color:var(--ink);background:rgba(255,252,243,.55);border:1px solid var(--line2);border-radius:6px;padding:14px 18px;cursor:pointer;transition:all .18s;line-height:1.6}
.opt:hover{border-color:rgba(169,123,20,.55);background:#fffdf6}
.opt code{font-family:var(--mono);font-size:13.5px}
.opt.right{border-color:var(--green);background:rgba(46,125,70,.1)}
.opt.wrong{border-color:var(--red);background:rgba(188,68,48,.09);animation:shake .4s ease}
.opt:disabled{cursor:default;opacity:.88}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.why{display:none;margin-top:14px;font-size:14px;line-height:1.8;color:var(--ink2);background:rgba(255,252,243,.6);border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.why.show{display:block}
.quiz-foot{display:flex;gap:12px;margin-top:22px;align-items:center;flex-wrap:wrap}
.score{font-family:var(--grot);color:var(--muted);font-size:13.5px}
/* preheat bar */
.pref-t{margin-left:auto;letter-spacing:.02em;font-size:12px;color:var(--muted);display:inline-flex;align-items:center;gap:6px;cursor:pointer;text-transform:none}
.pref-t input{accent-color:var(--gold);width:15px;height:15px;cursor:pointer}
.prebar{margin:0 0 12px;max-height:64px;overflow:hidden;transition:opacity .55s var(--ease),max-height .55s var(--ease),margin-bottom .55s var(--ease)}
.prebar.done{opacity:0;max-height:0;margin-bottom:0}
.pre-row{display:flex;justify-content:space-between;align-items:baseline;font-size:12px;color:var(--muted);margin-bottom:6px}
.pre-row b{font-family:var(--grot);font-weight:600;color:var(--gold);font-size:12.5px}
.pre-track{height:6px;border-radius:99px;background:rgba(84,66,28,.13);overflow:hidden}
.pre-fill{height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,var(--gold),var(--gold2));transition:width .55s ease}
/* coding judge */
.code-task{font-size:15px;line-height:1.85;color:var(--ink2);background:rgba(255,252,243,.6);border:1px solid var(--line);border-radius:12px;padding:15px 18px}
.code-task b{color:var(--gold)}
.editor{margin-top:14px;border-radius:14px;background:#171208;border:1px solid rgba(84,66,28,.4);overflow:hidden}
.editor .cb-bar{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid rgba(255,255,255,.09);background:rgba(255,255,255,.03)}
.editor .fn{font-family:var(--mono);font-size:12px;color:#b3a888;margin-left:8px}
.ed-wrap{display:flex;min-height:150px}
.ed-gutter{padding:14px 0;width:44px;flex:none;text-align:right;font-family:var(--mono);font-size:13.5px;line-height:1.8;color:#6e6249;border-right:1px solid rgba(255,255,255,.09);background:rgba(255,255,255,.02);overflow:hidden;user-select:none}
.ed-gutter div{padding-right:12px}
.ed-gutter .err-line{color:#ff9a86;font-weight:700}
#edCode{flex:1;background:transparent;border:none;outline:none;resize:vertical;min-height:150px;padding:14px 16px;font-family:var(--mono);font-size:13.5px;line-height:1.8;color:#f0e9d6;white-space:pre;overflow:auto;tab-size:2}
.code-fb{display:none;margin-top:14px;border-radius:12px;padding:16px 18px;font-size:14.5px;line-height:1.85;border:1px solid var(--line);background:rgba(255,252,243,.6)}
.code-fb.show{display:block}
.code-fb.pass{border-color:rgba(46,125,70,.55);background:rgba(46,125,70,.08)}
.code-fb.fail{border-color:rgba(188,68,48,.45);background:rgba(188,68,48,.06)}
.code-fb .fb-t{font-weight:700;font-size:15.5px}
.code-fb table{width:100%;border-collapse:collapse;margin-top:10px;font-family:var(--mono);font-size:12.8px}
.code-fb td,.code-fb th{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top;word-break:break-all}
.code-fb th{color:var(--muted);font-weight:500;background:rgba(169,123,20,.06)}
.code-fb tr.bad td{background:rgba(188,68,48,.1)}
.code-fb tr.ok td{color:#4d7a5c}
.code-fb .src-line{font-family:var(--mono);background:#171208;border-radius:8px;padding:8px 12px;margin-top:8px;font-size:13px;color:#ffb4a6;white-space:pre-wrap;word-break:break-all}
/* AI tutor */
.ai-thread{max-height:400px;overflow-y:auto;display:flex;flex-direction:column;gap:10px;padding:6px 2px}
.msg{max-width:88%;padding:11px 15px;border-radius:14px;font-size:14.5px;line-height:1.85;white-space:pre-wrap;word-break:break-word}
.msg.a{align-self:flex-start;background:rgba(255,252,243,.75);border:1px solid var(--line);border-bottom-left-radius:5px;color:var(--ink2)}
.msg.u{align-self:flex-end;background:rgba(169,123,20,.14);border:1px solid rgba(169,123,20,.4);border-bottom-right-radius:5px;color:#4c3a10}
.msg code{font-family:var(--mono);background:rgba(84,66,28,.1);padding:1px 6px;border-radius:5px;font-size:13px}
.msg.err{color:#a03424;border-color:rgba(188,68,48,.5)}
.ai-qrow{display:flex;gap:10px;margin-top:12px}
.ai-qrow input{flex:1;background:rgba(255,252,243,.7);border:1px solid var(--line2);border-radius:11px;color:var(--ink);font-size:14.5px;padding:12px 15px;outline:none;font-family:var(--sans)}
.ai-qrow input:focus{border-color:rgba(169,123,20,.6)}
/* settings */
.set-card{border-radius:18px;padding:28px clamp(20px,4vw,34px);margin-top:26px}
.set-card h3{font-family:var(--serif);font-weight:900;font-size:22px}
.ai-note{color:var(--ink2);font-size:13.5px;line-height:1.85;margin-top:12px}
.ai-lab{display:block;font-size:12px;letter-spacing:.14em;color:var(--muted);margin:18px 0 7px}
.ai-in{width:100%;background:rgba(255,255,255,.55);border:1px solid var(--line2);border-radius:11px;color:var(--ink);font-size:14.5px;padding:12px 15px;outline:none;font-family:var(--sans)}
.ai-in:focus{border-color:rgba(169,123,20,.6)}
select.ai-in option{background:#fffdf6}
.sh-nav{display:flex;gap:12px;margin:36px 0 60px;border-top:1px solid var(--line);padding-top:22px;align-items:center;flex-wrap:wrap}
.sh-nav .btn{padding:11px 24px;font-size:14px}
/* reveal */
.reveal{opacity:0;transform:translateY(26px);transition:opacity .8s ease,transform .8s cubic-bezier(.22,1.06,.36,1)}
.reveal.in{opacity:1;transform:none}
footer{border-top:1px solid var(--line);margin-top:30px}
footer .wrap{padding-top:34px;padding-bottom:56px;color:var(--muted);font-size:13px;line-height:2}
footer b{color:var(--ink2)}
#confetti{position:fixed;inset:0;z-index:120;pointer-events:none}
/* ---------- motion & glass audit fixes (space-edition spec) ---------- */
@keyframes lineIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes blockIn{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
@keyframes viewFade{from{opacity:0}to{opacity:1}}
.oline{animation:lineIn .42s cubic-bezier(.22,1,.36,1) both}
.cline{animation:lineIn .42s cubic-bezier(.22,1,.36,1) both}
.view.active{animation:viewFade .3s var(--ease)}
.view.active.leaving{opacity:0;transform:translateY(10px);transition:opacity .17s cubic-bezier(.22,1,.36,1),transform .17s cubic-bezier(.22,1,.36,1);animation:none}
.view.active>*,.view.active #lessonBody>*{animation:blockIn .5s cubic-bezier(.22,1,.36,1) both}
.view.active>*:nth-child(2),.view.active #lessonBody>*:nth-child(2){animation-delay:.05s}
.view.active>*:nth-child(3),.view.active #lessonBody>*:nth-child(3){animation-delay:.10s}
.view.active>*:nth-child(4),.view.active #lessonBody>*:nth-child(4){animation-delay:.15s}
.view.active>*:nth-child(5),.view.active #lessonBody>*:nth-child(5){animation-delay:.20s}
.view.active>*:nth-child(6),.view.active #lessonBody>*:nth-child(6){animation-delay:.25s}
.view.active #lessonBody>*:nth-child(7){animation-delay:.30s}
.view.active #lessonBody>*:nth-child(8){animation-delay:.35s}
.done-card{position:relative;overflow:hidden;background:linear-gradient(135deg,rgba(255,253,246,.66),rgba(255,246,222,.38));backdrop-filter:blur(20px) saturate(1.6);-webkit-backdrop-filter:blur(20px) saturate(1.6);border:1px solid rgba(255,255,255,.7);border-radius:22px;max-width:480px;width:100%;padding:34px clamp(24px,4vw,38px);text-align:center;box-shadow:inset 0 1px 0 rgba(255,255,255,.95),inset 0 -20px 34px rgba(255,255,255,.16),0 40px 90px rgba(60,45,5,.35);animation:viewIn .45s cubic-bezier(.22,1,.36,1)}
.done-card::before{content:'';position:absolute;inset:0;border-radius:inherit;background:linear-gradient(115deg,rgba(255,255,255,.55),rgba(255,255,255,0) 44%);pointer-events:none}
.done-card::after{content:'';position:absolute;inset:0;border-radius:inherit;box-shadow:inset 0 0 0 1px rgba(169,123,20,.14);pointer-events:none}
.done-check{width:76px;height:76px;margin:2px auto 16px;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 32% 26%,rgba(255,255,255,.85),rgba(243,229,187,.35) 55%,rgba(201,144,31,.18));border:1px solid rgba(169,123,20,.45);box-shadow:inset 0 2px 4px rgba(255,255,255,.9),inset 0 -8px 14px rgba(169,123,20,.18),0 16px 32px rgba(140,100,10,.22)}
.done-card h3{font-family:var(--serif);font-weight:900;font-size:25px;position:relative}
.done-card .mc-sub{position:relative}
.done-btns{display:flex;gap:12px;justify-content:center;margin-top:22px;position:relative;flex-wrap:wrap}
.code-fb table tr{animation:lineIn .42s cubic-bezier(.22,1,.36,1) both}
.code-fb table tr:nth-child(2){animation-delay:.06s}
.code-fb table tr:nth-child(3){animation-delay:.12s}
.code-fb table tr:nth-child(4){animation-delay:.18s}
.code-fb table tr:nth-child(5){animation-delay:.24s}
.code-fb table tr:nth-child(6){animation-delay:.30s}
/* ---------- major switch (release edition only) ---------- */
.segctl{display:inline-flex;border:1px solid var(--line2);border-radius:999px;overflow:hidden;background:rgba(255,252,243,.5)}
.segctl button{border:none;background:none;padding:7px 15px;font-size:12.5px;font-weight:700;color:var(--muted);cursor:pointer;font-family:var(--sans)}
.segctl button.on{background:linear-gradient(120deg,var(--gold2),var(--gold));color:#fff8e6}
.mode-modal{position:fixed;inset:0;z-index:200;background:rgba(43,33,8,.45);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);display:none;align-items:center;justify-content:center;padding:20px}
.mode-modal.open{display:flex}
.mode-card{background:var(--paper);border-radius:20px;max-width:620px;width:100%;padding:30px clamp(22px,4vw,36px);box-shadow:0 40px 100px rgba(60,45,5,.35);animation:viewIn .38s var(--ease)}
.mode-card h3{font-family:var(--serif);font-weight:900;font-size:24px}
.mode-card .mc-sub{color:var(--ink2);font-size:14px;line-height:1.85;margin-top:8px}
.mode-opts{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:20px}
.mode-opt{text-align:left;border:1px solid var(--line2);background:rgba(255,252,243,.6);border-radius:14px;padding:18px;cursor:pointer;font-family:var(--sans);transition:all .18s}
.mode-opt:hover{border-color:rgba(169,123,20,.6);background:#fffdf6;transform:translateY(-2px)}
.mode-opt .mo-t{font-family:var(--serif);font-weight:900;font-size:18px}
.mode-opt .mo-d{color:var(--muted);font-size:13px;line-height:1.7;margin-top:6px}
.mode-skip{margin-top:18px;text-align:center}
.mode-skip button{background:none;border:none;color:var(--muted);font-size:13.5px;cursor:pointer;text-decoration:underline}
@media(max-width:640px){.mode-opts{grid-template-columns:1fr}.segctl button{padding:7px 11px}}
@media(max-width:760px){
  .ide-body{grid-template-columns:1fr}
  .ide-console{border-left:none;border-top:1px solid rgba(255,255,255,.09)}
  .lrow .no{min-width:44px}
  .masthead span:nth-child(2){display:none}
  .navlink.hideS{display:none}
}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.001s!important;transition-duration:.001s!important}
  html{scroll-behavior:auto}
}
</style>
</head>
<body>
<nav><div class="nav-in">
  <div class="logo" id="logoHome">PYTHON <b>自学教程</b> · 空间版</div>
  <div class="sp"></div>
  <button class="navlink hideS" id="navRoute">学习路线</button>
  <span class="segctl" id="modeSegNav"><button data-mode="accounting">会计</button><button data-mode="general">通用</button></span>
  <button class="navlink" id="navSettings">设置 · AI Key</button>
  <div class="ringwrap"><span id="ringTxt">已完成 0 / 41 课</span><span class="xp" id="xpLab">0 XP</span></div>
</div></nav>

<main id="homeView" class="view active"><div class="wrap">
  <div class="masthead"><span>PYTHON 自学教程 · 空间版</span><span>41 课 · 164 题 · 1120 分钟</span><span>下载版 · 二〇二六</span></div>
  <header class="hero">
    <div class="ghost" aria-hidden="true">Py</div>
    <div class="kicker">A Self-Taught Path</div>
    <h1>把 Python<br>一课一课<span class="accent">走完</span>。</h1>
    <p class="sub">从第一行 print，到亲手做出一份<span id="heroReport">账本报告</span>——41 课、123 道选择题加 41 道动手编程题，每课都有会动的代码演示；你写的代码会被真的运行、逐行判定对错。进度只保存在这台设备的浏览器里，随时回来接着走。</p>
    <div class="cta">
      <button class="btn btn-gold" id="ctaStart">开始学习 →</button>
      <button class="btn btn-ghost" id="ctaRoute">看学习路线</button>
    </div>
    <div class="stats reveal">
      <div class="stat"><div class="n"><span data-count="41">0</span><em> 课</em></div><div class="t">LESSONS</div></div>
      <div class="stat"><div class="n"><span data-count="164">0</span><em> 题</em></div><div class="t">选择题 + 动手编程题</div></div>
      <div class="stat"><div class="n"><span data-count="1120">0</span><em> 分钟</em></div><div class="t">总时长</div></div>
      <div class="stat"><div class="n"><span data-count="5">0</span><em> 阶段</em></div><div class="t" id="statsStages">地基 · 工具 · 会计应用 · 进阶应用 · 网络与爬虫</div></div>
    </div>
    <div class="progress-card glass reveal">
      <div><div class="pc-t">我的进度 · 本机保存</div><div class="pc-n" id="pcText">0 / 41 课</div></div>
      <div class="pc-bar"><i id="pcFill" style="width:0%"></i></div>
      <button class="btn btn-gold" id="pcGo" style="padding:11px 24px;font-size:14px">继续学习</button>
    </div>
    <div class="ide reveal" id="heroIde">
      <div class="ide-bar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span><span class="ide-tab" id="heroFile">hello.py</span></div>
      <div class="ide-body">
        <div class="ide-code" id="heroCode"></div>
        <div class="ide-console"><div class="hd">运行结果 · CONSOLE</div><div id="heroOut"></div></div>
      </div>
    </div>
  </header>

  <section class="route" id="route">
    <div class="route-head reveal">
      <h2>学习路线</h2>
      <p>一条线走到底：学完一课，进度就向前走一格。点任意一课开始——讲解、代码演示、练习，都在里面。每课都标了预估难度与用时。</p>
    </div>
    <div class="search reveal"><span style="color:var(--muted2)">⌕</span><input id="searchBox" type="text" placeholder="搜索课程，例如：循环、字典、pandas…"></div>
    <div class="achv reveal" id="achvRow"></div>
    <div id="stages"></div>
    <div class="empty" id="emptyMsg">没有找到匹配的课程，换个关键词试试。</div>
  </section>
</div></main>

<main id="lessonView" class="view"><div class="wrap">
  <button class="backbtn" id="backHome">← 回到学习路线</button>
  <div id="lessonBody"></div>
</div></main>

<main id="settingsView" class="view"><div class="wrap">
  <div class="masthead"><span>设置</span><span>专业方向 · AI API KEY</span><span>只存本机</span></div>
  <div class="set-card" style="border:1px solid var(--line);background:rgba(255,252,243,.5);box-shadow:none">
    <h3>专业方向</h3>
    <p class="ai-note">这套教程的第三阶段与几个综合项目原本是按会计专业的场景写的（账本、记账）。如果你不是会计专业，可以切换到「通用」方向：同一套代码与练习，只把场景表述换成消费记录、销售数据、数据报表等通用说法。切换立即生效，选择只存在本机浏览器。</p>
    <div class="quiz-foot" style="margin-top:16px"><span class="segctl" id="modeSegSet"><button data-mode="accounting">会计方向</button><button data-mode="general">通用方向</button></span><span class="score" id="modeState"></span></div>
  </div>
  <div class="set-card glass">
    <h3>接入你自己的 AI（可选）</h3>
    <p class="ai-note">填入你自己的 AI 接口和 API Key，就能在每一课里向 AI 导师提问、要讲解。Key 只保存在你这台设备的浏览器（localStorage）里，本文件没有任何服务器，不会上传你的 Key；调用产生的费用算在你自己的账号上。不填也完全不影响学完全部课程。</p>
    <label class="ai-lab">服务商预设（OpenAI 兼容接口）</label>
    <select id="aiPreset" class="ai-in"></select>
    <label class="ai-lab">接口地址（Base URL）</label>
    <input id="aiBase" class="ai-in" type="text" placeholder="https://api.openai.com/v1" autocomplete="off">
    <label class="ai-lab">API Key</label>
    <input id="aiKey" class="ai-in" type="password" placeholder="sk-…" autocomplete="off">
    <label class="ai-lab">模型名</label>
    <input id="aiModel" class="ai-in" type="text" placeholder="例如 gpt-4o-mini 或 deepseek-chat" autocomplete="off">
    <div class="quiz-foot" style="margin-top:22px">
      <button class="btn btn-gold" id="aiSave" style="padding:11px 26px;font-size:14px">保存设置</button>
      <button class="btn btn-ghost" id="aiClear" style="padding:11px 22px;font-size:14px">清除 Key</button>
      <span class="score" id="aiState"></span>
    </div>
    <p class="ai-note">提示：接口需要支持浏览器跨域调用（CORS）。若某家接口在浏览器里调不通，换一家支持跨域的兼容接口即可；这与 Key 本身无关。</p>
  </div>
  <div class="set-card" style="border:1px solid var(--line);background:rgba(255,252,243,.5);box-shadow:none">
    <h3>数据说明</h3>
    <p class="ai-note">学习进度、答题记录、成就与 AI 对话都只存在本机浏览器的 localStorage 中，初始为空，从你第一次打开开始累计。清除浏览器数据会一并清掉这些记录。本文件除代码判定所需的 Python 运行环境（Pyodide，联网时从 CDN 加载）外，不依赖任何外部文件；断网时课文、选择题与代码演示照常可用。</p>
    <div class="quiz-foot"><button class="btn btn-ghost" id="wipeBtn" style="padding:10px 22px;font-size:13.5px">清除全部学习记录</button><span class="score" id="wipeState"></span></div>
  </div>
  <div style="height:56px"></div>
</div></main>

<footer><div class="wrap">
  <b>Python 自学教程 · 空间版</b> —— 单文件下载版，双击即可打开学习。<br>
  课程共 41 课 / 5 个阶段；代码判定在你的浏览器本地运行，学习数据不离开这台设备。
</div></footer>
<canvas id="confetti"></canvas>
<div class="mode-modal" id="doneModal"><div class="done-card">
  <div class="done-check"><svg viewBox="0 0 24 24" width="38" height="38" fill="none"><path d="M4.5 12.6l5 5L19.5 6.8" stroke="#8a6410" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
  <h3>这一课，学完了</h3>
  <p class="mc-sub" id="doneSub"></p>
  <div class="done-btns"><button class="btn btn-gold" id="doneNext">下一课 →</button><button class="btn btn-ghost" id="doneRoute">返回路线</button></div>
</div></div>
<div class="mode-modal" id="modeModal"><div class="mode-card">
  <div class="stg">开始之前 · 选一个方向</div>
  <h3>你的专业方向是？</h3>
  <p class="mc-sub">这套教程第三阶段和几个综合项目备了两种场景表述：会计方向用账本、记账的例子；通用方向用消费记录、销售数据、数据报表的例子。代码、练习和判定完全一样，随时可以在设置页或页面顶部切换。</p>
  <div class="mode-opts">
    <button class="mode-opt" data-pick="accounting"><div class="mo-t">会计方向</div><div class="mo-d">默认方向。场景贴合会计专业：账本汇总、记账统计、年度账本报告。</div></button>
    <button class="mode-opt" data-pick="general"><div class="mo-t">通用方向</div><div class="mo-d">面向其他专业与兴趣学习者：消费记录、销售数据、数据报表等通用场景。</div></button>
  </div>
  <div class="mode-skip"><button id="modeSkip">跳过，先用默认（会计方向）</button></div>
</div></div>
<script>
const STAGES = __STAGES_JSON__;
const LESSONS = __LESSONS_JSON__;
const MEALS_CSV = __MEALS_JSON__;
const LEDGER_CSV = __LEDGER_JSON__;
</script>
<script>
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const LS_MAIN='pytut-space-v1', LS_PREF='pytut-space-pref', LS_AI='pytut-space-ai', LS_CHATS='pytut-space-ai-chats';
function loadJSON(k, dft){ try{ const v=JSON.parse(localStorage.getItem(k)||'null'); return v==null? dft : v; }catch(e){ return dft; } }
const store=Object.assign({done:[],best:{},codeDone:[],answers:{}}, loadJSON(LS_MAIN,{}));
const save=()=>{ try{ localStorage.setItem(LS_MAIN,JSON.stringify(store)); }catch(e){} };
const pref=Object.assign({preheat:true}, loadJSON(LS_PREF,{}));
const savePref=()=>{ try{ localStorage.setItem(LS_PREF,JSON.stringify(pref)); }catch(e){} };
const doneSet=new Set(store.done);
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function hl(code){
  let s=esc(code);
  s=s.replace(/(#[^\n]*)|((?:f|b|r)?"(?:[^"\\]|\\.)*"|(?:f|b|r)?'(?:[^'\\]|\\.)*')|\b(import|from|as|def|return|if|elif|else|for|while|in|not|and|or|try|except|with|True|False|None)\b|\b(\d+(?:\.\d+)?)\b|\b(print|len|range|float|int|str|type|input|sum|round|open|list|dict|append|sort|split|strip|read|write|values|keys|groupby|read_csv|bar|savefig|weekday|date)\b/g,
   (m,cm,str,kw,num,fn)=> cm?'<span class="tok-cm">'+cm+'</span>' : str?'<span class="tok-str">'+str+'</span>' : kw?'<span class="tok-kw">'+kw+'</span>' : num?'<span class="tok-num">'+num+'</span>' : '<span class="tok-fn">'+fn+'</span>');
  return s;
}
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const DIFF_LAB={1:'入门',2:'基础',3:'进阶',4:'挑战',5:'综合'};
function diffSeg(n){ let s='<span class="diff" aria-hidden="true">'; for(let k=1;k<=5;k++) s+='<i class="'+(k<=n?'on':'')+'"></i>'; return s+'</span>'; }
const PLATE=['其一','其二','其三','其四','其五'];
/* ---------- views ---------- */
let curView='home';
function showView(name){
  const to=$('#'+name+'View'); if(!to) return;
  const from=document.querySelector('.view.active');
  const swap=()=>{ ['home','lesson','settings'].forEach(v=>{ $('#'+v+'View').classList.toggle('active', v===name); }); curView=name; window.scrollTo({top:0, behavior:'auto'}); if(name==='home'){ renderRoute(); } if(name==='settings'){ fillSettings(); } };
  if(from&&from!==to&&!reduced){ from.classList.add('leaving'); setTimeout(()=>{ from.classList.remove('leaving'); swap(); },170); } else swap();
}
$('#logoHome').onclick=()=>showView('home');
$('#navRoute').onclick=()=>{ showView('home'); setTimeout(()=>document.getElementById('route').scrollIntoView({behavior:reduced?'auto':'smooth'}),300); };
$('#navSettings').onclick=()=>showView('settings');
$('#backHome').onclick=()=>showView('home');
/* ---------- route ---------- */
let gidx=0; LESSONS.forEach(l=>l.gi=gidx++);
function firstOpen(){ const i=LESSONS.findIndex(l=>!doneSet.has(l.gi)); return i<0?LESSONS.length-1:i; }
function xpNow(){ return doneSet.size*50+(store.codeDone||[]).length*30+Object.values(store.best||{}).reduce((a,b)=>a+(+b||0),0)*10; }
function renderRoute(){
  const wrap=$('#stages'); if(!wrap) return; wrap.innerHTML='';
  STAGES.forEach((st,si)=>{
    const items=LESSONS.map((l,i)=>({l,i})).filter(x=>x.l.stage===si);
    const dn=items.filter(x=>doneSet.has(x.l.gi)).length;
    const sec=document.createElement('section'); sec.className='stage reveal';
    sec.innerHTML=`<div class="stage-head"><span class="plate">${PLATE[si]} · 阶段${st.medal}</span><h3>${st.name}</h3><div class="stage-bar"><i style="width:${dn/items.length*100}%"></i></div><div class="stage-pct">${dn}/${items.length}</div><div class="ss">${st.sub}</div></div>
    <div class="lrows">${items.map(({l,i})=>{
      const d=doneSet.has(l.gi), cur=l.gi===firstOpen();
      return `<div class="lrow ${d?'done':''}" data-open="${i}" data-title="${esc(l.title)}" tabindex="0" role="button" aria-label="打开第 ${l.gi+1} 课">
        <div class="no">${String(l.gi+1).padStart(2,'0')}</div>
        <div class="main"><h4>${esc(l.title)}</h4><p>${esc(l.intro)}</p></div>
        <div class="side"><span class="meta">${l.mins} 分钟 · ${l.quiz.length} 题 + 动手写 · 难度 ${DIFF_LAB[l.diff]}${diffSeg(l.diff)}</span><br><span class="status ${d?'done':cur?'cur':''}">${d?'✓ 已完成':cur?'当前课程':'未开始'}</span></div>
      </div>`}).join('')}
    </div><div class="flag">阶段${st.medal} · 还剩 ${items.length-dn} 课</div>`;
    wrap.appendChild(sec);
  });
  wrap.querySelectorAll('.lrow').forEach(r=>{
    r.addEventListener('click',()=>openLesson(+r.dataset.open));
    r.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); openLesson(+r.dataset.open); } });
  });
  updateProgress(); renderAchv(); observeReveals();
}
function updateProgress(){
  const n=doneSet.size;
  $('#ringTxt').textContent=`已完成 ${n} / ${LESSONS.length} 课`;
  $('#xpLab').textContent=xpNow()+' XP';
  const pc=$('#pcText'); if(pc) pc.textContent=`${n} / ${LESSONS.length} 课`;
  const pf=$('#pcFill'); if(pf) pf.style.width=(n/LESSONS.length*100)+'%';
}
function renderAchv(){
  const row=$('#achvRow'); if(!row) return;
  const stTot={}, stDone={}; LESSONS.forEach(l=>{ stTot[l.stage]=(stTot[l.stage]||0)+1; if(doneSet.has(l.gi)) stDone[l.stage]=(stDone[l.stage]||0)+1; });
  const B=[['初露锋芒','完成第 1 课',doneSet.size>=1]];
  STAGES.forEach((st,si)=>{ B.push([st.name+'全清','完成阶段'+st.medal+'的全部课程',!!(stTot[si]&&(stDone[si]||0)>=stTot[si])]); });
  B.push(['代码工匠','动手题通过 10 课',(store.codeDone||[]).length>=10]);
  B.push(['半程英雄','完成 21 课',doneSet.size>=21]);
  B.push(['大满贯','全部课程完成',doneSet.size>=LESSONS.length]);
  row.innerHTML=B.map(b=>`<span class="bdg ${b[2]?'on':''}" title="${b[1]}">${b[2]?'✓ ':''}${b[0]}</span>`).join('');
}
/* ---------- reveal & countup ---------- */
let io;
function observeReveals(){ if(io) io.disconnect();
  if(!('IntersectionObserver' in window)){ $$('.reveal').forEach(el=>el.classList.add('in')); return; }
  io=new IntersectionObserver(es=>es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }),{threshold:.08});
  $$('.reveal').forEach(el=>io.observe(el));
}
const cio=('IntersectionObserver' in window)? new IntersectionObserver(es=>es.forEach(e=>{ if(!e.isIntersecting) return; cio.unobserve(e.target);
  const end=+e.target.dataset.count, t0=performance.now();
  (function tick(t){ const p=Math.min(1,(t-t0)/1100); e.target.textContent=Math.round(end*(1-Math.pow(1-p,3))).toString(); if(p<1) requestAnimationFrame(tick); else e.target.textContent=end; })(t0);
}),{threshold:.4}) : null;
if(cio) $$('[data-count]').forEach(el=>cio.observe(el)); else $$('[data-count]').forEach(el=>el.textContent=el.dataset.count);
/* ---------- hero typing ---------- */
const SNIPS=[
 {f:'hello.py', l:0},
 {f:'variables.py', l:1},
 {f:'loop.py', l:11}];
let snipI=0;
async function heroLoop(){
  const codeEl=$('#heroCode'), outEl=$('#heroOut'), fileEl=$('#heroFile'); if(!codeEl) return;
  const wait=ms=>new Promise(r=>setTimeout(r,ms));
  while(true){
    if(curView!=='home'){ await wait(900); continue; }
    const s=SNIPS[snipI%SNIPS.length]; snipI++;
    const L0=LESSONS[s.l]; fileEl.textContent=s.f; outEl.innerHTML=''; codeEl.innerHTML='';
    if(reduced){ codeEl.innerHTML=hl(L0.code); outEl.innerHTML=L0.out.map(o=>esc(o)).join('<br>'); await wait(4000); continue; }
    const plain=L0.code; let buf='';
    codeEl.innerHTML='<span class="caret"></span>';
    for(const ch of plain){ buf+=ch; codeEl.innerHTML=esc(buf)+'<span class="caret"></span>'; let dly=38+Math.random()*46; if(ch==='\n') dly=300+Math.random()*160; else if(ch===':'||ch===','||ch==='(') dly+=64; await wait(dly); }
    codeEl.innerHTML=hl(plain); await wait(560);
    for(const line of L0.out){ outEl.innerHTML+=(outEl.innerHTML?'<br>':'')+esc(line); await wait(360+Math.random()*240); }
    await wait(3200);
  }
}
/* ---------- lesson ---------- */
let cur=-1, quizSel=[], quizPos=0, quizLock=false, demoSeq=0;
function openLesson(i){
  cur=i; quizSel=LESSONS[i].quiz.map(()=>null); quizPos=0; quizLock=false; demoSeq++;
  const l=LESSONS[i], st=STAGES[l.stage];
  $('#lessonBody').innerHTML=`
   <div class="lesson-head"><div class="ghost" aria-hidden="true">${String(l.gi+1).padStart(2,'0')}</div>
     <div class="stg">${PLATE[l.stage]} · 阶段${st.medal} ${st.name} — LESSON ${l.gi+1} / ${LESSONS.length} · 难度 ${DIFF_LAB[l.diff]}${diffSeg(l.diff)}</div>
     <h3>${esc(l.title)}</h3></div>
   <div class="sec-t">讲解</div>
   <div class="intro">${dispExplain(l)}</div>
   <div class="tip"><b>注意 ·</b> ${esc(l.tip)}</div>
   <div class="sec-t">代码演示</div>
   <div class="demo-plate glass"><div class="codebox" id="demoBox"><div class="cb-bar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span><span class="fn">demo.py</span><button class="runbtn" id="runBtn">▶ 运行演示</button></div>
   <pre id="demoCode">${hl(l.code)}</pre>
   <div class="console" id="demoCon"><div class="hd">运行结果</div><div id="demoOut"></div></div></div></div>
   <div class="sec-t">互动练习 · ${l.quiz.length} 题</div>
   <div id="quizBox"></div>
   <div class="sec-t">动手写 · 即刻判定<label class="pref-t" title="打开课程时在后台提前加载 Python 运行环境，写代码时不用等冷启动"><input type="checkbox" id="prefHeat">预热运行环境</label></div>
   <div class="prebar" id="preBar" hidden><div class="pre-row"><span id="preLab">正在加载运行环境</span><b id="prePct">0%</b></div><div class="pre-track"><div class="pre-fill" id="preFill"></div></div></div>
   <div id="codeBox"></div>
   <div class="sec-t">AI 导师 · 接入自己的 AI</div>
   <div id="aiBox"></div>
   <div class="sh-nav">
     <button class="btn btn-ghost" id="prevBtn" ${i===0?'disabled':''}>← 上一课</button>
     <button class="btn btn-ghost" id="nextBtn" ${i===LESSONS.length-1?'disabled':''}>下一课 →</button>
     <span style="flex:1"></span>
     <span class="score" id="doneState">${doneSet.has(l.gi)?'✓ 本课已完成':'完成练习后点亮本课'}</span>
   </div>`;
  showView('lesson');
  const ph=$('#prefHeat'); if(ph){ ph.checked=!!pref.preheat; ph.onchange=()=>{ pref.preheat=ph.checked; savePref(); if(ph.checked){ try{ startPreheat(); }catch(e){} } else { const b=$('#preBar'); if(b) b.hidden=true; } }; }
  if(pref.preheat){ try{ startPreheat(); }catch(e){} }
  $('#prevBtn').onclick=()=>{ if(cur>0) openLesson(cur-1); };
  $('#nextBtn').onclick=()=>{ if(cur<LESSONS.length-1) openLesson(cur+1); };
  $('#runBtn').onclick=()=>runDemo();
  const db=$('#demoBox');
  if(db && !reduced && 'IntersectionObserver' in window){ const mySeq=demoSeq;
    const dio=new IntersectionObserver(es=>{ es.forEach(e=>{ if(e.intersectionRatio>=0.5){ dio.disconnect(); const b=$('#runBtn'); if(mySeq===demoSeq && b && !b.disabled && b.textContent.indexOf('再跑')<0) runDemo(); } }); },{threshold:[0.5]});
    dio.observe(db); }
  renderQuiz(); renderCoding(); renderAiBox();
}
async function runDemo(){
  const l=LESSONS[cur], btn=$('#runBtn'), pre=$('#demoCode'), con=$('#demoCon'), out=$('#demoOut'); if(!btn) return;
  const mySeq=++demoSeq;
  btn.disabled=true; btn.textContent='运行中…'; con.classList.remove('show'); out.innerHTML='';
  const wait=ms=>new Promise(r=>setTimeout(r,ms));
  if(reduced){ pre.innerHTML=hl(l.code); }
  else{ let buf=''; for(const ch of l.code){ if(mySeq!==demoSeq) return; buf+=ch; pre.textContent=buf; let dly=38+Math.random()*46; if(ch==='\n') dly=300+Math.random()*160; else if(ch===':'||ch===','||ch==='(') dly+=64; await wait(dly); } pre.innerHTML=hl(l.code); }
  if(mySeq!==demoSeq) return;
  await wait(560); if(mySeq!==demoSeq) return; con.classList.add('show');
  for(const line of l.out){ if(mySeq!==demoSeq) return; const d=document.createElement('div'); d.className='oline'; d.textContent=line; out.appendChild(d); await wait(360+Math.random()*240); }
  btn.disabled=false; btn.textContent='↻ 再跑一次';
}
function renderQuiz(){
  const l=LESSONS[cur], box=$('#quizBox'); if(!box) return;
  const q=l.quiz[quizPos], sel=quizSel[quizPos];
  const answered=quizSel.filter(x=>x!==null).length;
  if(answered===l.quiz.length&&sel===null){ renderQuizResult(); return; }
  box.innerHTML=`<div class="qdots">${l.quiz.map((_,k)=>`<i class="${quizSel[k]===null?(k===quizPos?'now':''):quizSel[k]===l.quiz[k].ans?'ok':'bad'}"></i>`).join('')}</div>
   <div class="quiz-q">第 ${quizPos+1} 题 · ${esc(q.q)}</div>
   <div class="opts">${q.opts.map((o,k)=>{ let cls=''; if(sel!==null){ if(k===q.ans) cls='right'; else if(k===sel) cls='wrong'; }
     return `<button class="opt ${cls}" data-k="${k}" ${sel!==null?'disabled':''}>${esc(o)}</button>`; }).join('')}</div>
   <div class="why ${sel!==null?'show':''}">${sel!==null?('<b>'+(sel===q.ans?'✓ 答对了。':'✗ 答错了。')+'</b> '+esc(q.why)):''}</div>
   <div class="quiz-foot">${sel!==null?`<button class="btn btn-gold" id="qNext" style="padding:11px 26px;font-size:14px">${quizPos<l.quiz.length-1?'下一题 →':'查看结果'}</button>`:''}
   <span class="score">已答 ${answered} / ${l.quiz.length}</span></div>`;
  box.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{ if(quizLock) return; quizLock=true; const k=+b.dataset.k; quizSel[quizPos]=k; store.answers[l.gi+'-'+quizPos]=k; save(); setTimeout(()=>{ quizLock=false; renderQuiz(); },60); });
  const nx=$('#qNext'); if(nx) nx.onclick=()=>{ if(quizPos<l.quiz.length-1){ quizPos++; renderQuiz(); } else renderQuizResult(); };
}
function renderQuizResult(){
  const l=LESSONS[cur], score=quizSel.reduce((a,s,k)=>a+(s===l.quiz[k].ans?1:0),0);
  const prevBest=store.best[l.gi]||0; if(score>prevBest){ store.best[l.gi]=score; save(); }
  $('#quizBox').innerHTML=`<div class="qdots">${l.quiz.map((q,k)=>`<i class="${quizSel[k]===q.ans?'ok':'bad'}"></i>`).join('')}</div>
   <div class="quiz-q">${score===l.quiz.length?'全对，漂亮！':score===l.quiz.length-1?'就差一题，全对在望。':'这一课先记个大概，错题讲解都在上面。'}</div>
   <div class="why show">本课得分 <b>${score} / ${l.quiz.length}</b>${prevBest?` · 历史最佳 ${Math.max(prevBest,score)} / ${l.quiz.length}`:''}。${score<l.quiz.length?'点「再练一次」可以重做错题思路，讲解会再看一遍。':'点下面按钮点亮这一课，进度会向前走一格。'}</div>
   <div class="quiz-foot">
     <button class="btn btn-ghost" id="qRetry" style="padding:11px 24px;font-size:14px">再练一次</button>
     ${doneSet.has(l.gi)?'<span class="score">✓ 本课已完成</span>':`<button class="btn btn-gold" id="qDone" style="padding:11px 26px;font-size:14px">完成本课 ✓</button>`}
   </div>`;
  $('#qRetry').onclick=()=>{ quizSel=LESSONS[cur].quiz.map(()=>null); quizPos=0; renderQuiz(); };
  const dn=$('#qDone'); if(dn) dn.onclick=completeLesson;
}
function completeLesson(){
  const l=LESSONS[cur]; doneSet.add(l.gi); store.done=[...doneSet]; save();
  const ds=$('#doneState'); if(ds) ds.textContent='✓ 本课已完成'; confettiBurst();
  renderQuizResult(); updateProgress();
  const nx=$('#nextBtn'); if(nx&&cur<LESSONS.length-1){ nx.textContent='下一课 → 已解锁'; }
  if(doneSet.size===LESSONS.length){ setTimeout(()=>confettiBurst(true),450); }
  showDoneOverlay(l);
}
function showDoneOverlay(l){
  const m=$('#doneModal'); if(!m) return;
  $('#doneSub').textContent='第 '+(cur+1)+' 课《'+l.title+'》已点亮，+50 XP。'+(cur<LESSONS.length-1?'顺着势头，下一课已经解锁。':'全部 41 课都完成了，漂亮！');
  $('#doneNext').style.display=cur<LESSONS.length-1?'':'none';
  m.classList.add('open');
}
$('#doneNext').onclick=()=>{ $('#doneModal').classList.remove('open'); if(cur<LESSONS.length-1) openLesson(cur+1); };
$('#doneRoute').onclick=()=>{ $('#doneModal').classList.remove('open'); showView('home'); };
/* ---------- confetti ---------- */
const cv=$('#confetti'), cx2=cv.getContext('2d'); let parts=[], rafId=null;
function sizeCv(){ cv.width=innerWidth; cv.height=innerHeight; } sizeCv(); addEventListener('resize',sizeCv);
function confettiBurst(big=false){
  if(reduced) return;
  const colors=['#c1901f','#a97b14','#f3e5bb','#2e7d46'];
  const n=big?150:70;
  for(let k=0;k<n;k++){ parts.push({x:innerWidth/2+(Math.random()-.5)*260, y:innerHeight*0.32, vx:(Math.random()-.5)*(big?13:9), vy:-Math.random()*9-4, g:.28, s:Math.random()*7+4, r:Math.random()*Math.PI, vr:(Math.random()-.5)*.3, c:colors[k%colors.length], life:1, decay:.006+Math.random()*.006}); }
  if(!rafId) confettiTick();
}
function confettiTick(){
  cx2.clearRect(0,0,cv.width,cv.height);
  parts=parts.filter(p=>p.life>0&&p.y<innerHeight+30);
  for(const p of parts){ p.x+=p.vx; p.y+=p.vy; p.vy+=p.g; p.r+=p.vr; p.life-=p.decay;
    cx2.save(); cx2.translate(p.x,p.y); cx2.rotate(p.r); cx2.globalAlpha=Math.max(0,p.life); cx2.fillStyle=p.c; cx2.fillRect(-p.s/2,-p.s/2,p.s,p.s*.62); cx2.restore(); }
  if(parts.length){ rafId=requestAnimationFrame(confettiTick); } else { rafId=null; cx2.clearRect(0,0,cv.width,cv.height); }
}
/* ---------- hands-on judge: real Python in the browser (Pyodide, main thread — file:// friendly) ---------- */
const PY_CDN='https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';
let pyodideObj=null, pyLoading=null, pyWarm=false, pyBaseReady=false;
const pyLoadedPkgs={};
const codeCache={}, lastJudge={};
function loadScriptOnce(src){ return new Promise((res,rej)=>{ const s=document.createElement('script'); s.src=src; s.onload=res; s.onerror=()=>rej(new Error('script load failed')); document.head.appendChild(s);});}
function ensurePy(){
if(pyodideObj) return Promise.resolve(pyodideObj);
if(pyLoading) return pyLoading;
pyLoading=(async()=>{
if(typeof loadPyodide==='undefined') await loadScriptOnce(PY_CDN+'pyodide.js');
pyodideObj=await loadPyodide({indexURL:PY_CDN});
pyBaseReady=true; onPyProgress('base');
return pyodideObj;
})();
pyLoading.catch(()=>{ pyLoading=null;});
return pyLoading;
}
async function ensurePkgs(py, pkgs){
for(const p of (pkgs||[])){
if(pyLoadedPkgs[p]) continue;
if(p.indexOf('pip:')===0){
if(!pyLoadedPkgs.__mp){ await py.loadPackage('micropip'); pyLoadedPkgs.__mp=1;}
const mp=py.pyimport('micropip'); await mp.install(p.slice(4));
} else { await py.loadPackage(p);}
pyLoadedPkgs[p]=1;
}
}
async function runStudentCode(code, pkgs, files, checkFile){
const py=await ensurePy();
await ensurePkgs(py, pkgs);
const fs=(files||{}); for(const k in fs){ try{ py.FS.writeFile(k, fs[k]);}catch(e){}}
const out=[]; py.setStdout({batched:s=>out.push(s)}); py.setStderr({batched:s=>out.push(s)});
const r={ok:true, out};
try{ await py.runPythonAsync(code);}catch(err){ r.ok=false; r.error=String(err&&err.message?err.message:err);}
if(checkFile){ try{ r.fileExists=!!py.FS.analyzePath(checkFile).exists;}catch(e){ r.fileExists=false;}}
return r;
}
function setPre(pct, lab){ const f=$('#preFill'), p=$('#prePct'), l=$('#preLab'); if(f) f.style.width=pct+'%'; if(p) p.textContent=pct+'%'; if(l&&lab) l.textContent=lab;}
function onPyProgress(stage){ if(stage==='base'){ const b=$('#preBar'); if(b&&!b.hidden) setPre(60,'运行环境已就绪 · 正在加载工具包');}}
function startPreheat(){
const bar=$('#preBar'); if(!pref.preheat){ if(bar) bar.hidden=true; return;}
if(!bar) return;
bar.hidden=false; bar.classList.remove('done');
if(pyBaseReady) setPre(85,'运行环境已就绪 · 正在加载工具包'); else setPre(12,'正在加载运行环境');
const l=LESSONS[cur], pkgs=(l&&l.coding&&l.coding.pkgs)||[];
(async()=>{ try{ const py=await ensurePy(); await ensurePkgs(py, pkgs); pyWarm=true; setPre(100,'就绪 · 写代码时不用等了');}
catch(e){ setPre(100,'预热未完成 · 判定时会自动加载');}
const b=$('#preBar'); if(b){ setTimeout(()=>{ b.classList.add('done'); setTimeout(()=>{ b.hidden=true;},620);},1000);}
})();
}
const ERR_ZH={SyntaxError:'语法错误——多半是冒号、引号或括号没配对好。',IndentationError:'缩进错误——Python 靠缩进分代码块，该缩进的行要对齐。',NameError:'名字错误——变量名可能打错了，或者用之前还没赋值。',TypeError:'类型错误——比如字符串和数字直接相加，要先用 float() / int() 转换。',ValueError:'值不对——比如把不是数字的文字拿去 float()。',KeyError:'键不存在——字典里没有这个键，检查键名拼写。',IndexError:'下标越界——列表没有这么多元素，下标从 0 开始数。',ZeroDivisionError:'除以 0 了——除数不能是 0。',FileNotFoundError:'文件不存在——检查文件名和打开模式。',ModuleNotFoundError:'库导入失败——检查 import 的库名。',AttributeError:'属性/方法不存在——检查方法名拼写，比如 append、sort。'};
function errLineOf(s){ const m=[...String(s).matchAll(/line (\d+)/g)]; return m.length?+m[m.length-1][1]:0;}
const ZHMAP={'學':'学','習':'习','優':'优','圖':'图','總':'总','貴':'贵','筆':'笔','項':'项','滿':'满','數':'数','據':'据','讀':'读','寫':'写','檔':'档','錯':'错','麼':'么','這':'这','裡':'里','開':'开','點':'点','時':'时','長':'长','個':'个','們':'们','為':'为','應':'应','該':'该','會':'会','讓':'让','變':'变','環':'环','節':'节','錄':'录','統':'统','計':'计','價':'价','錢':'钱','買':'买','賣':'卖','飯':'饭','麵':'面','乾':'干','後':'后','過':'过','還':'还','進':'进','遠':'远','運':'运','動':'动','場':'场','國':'国','現':'现','實':'实','際':'际','發':'发','將':'将','對':'对','來':'来','說':'说','請':'请','謝':'谢','歡':'欢','迎':'迎'};
function normLine(s){ return String(s).replace(/[學學習優圖總貴筆項滿數據讀寫檔錯麼這裡開點時長個們為應該會讓變環節錄統計價錢買賣飯麵乾後過還進遠運動場國現實際發將對來說請謝歡迎]/g, ch=>ZHMAP[ch]||ch);}
const PUNCT={'，':',','。':'.','：':':','！':'!','？':'?','；':';','（':'(','）':')','“':'"','”':'"','‘':"'",'’':"'",'、':','};
function normBase(s){ return normLine(s).replace(/[，。：！？；（）“”‘’、]/g, ch=>PUNCT[ch]||ch);}
function judgeEq(e, a){
const x=normBase(e).replace(/\s+/g,''), y=normBase(a).replace(/\s+/g,'');
if(x===y) return true;
const nums=s=>[...s.matchAll(/-?\d+\.?\d*/g)].map(m=>parseFloat(m[0]));
const skel=s=>s.replace(/-?\d+\.?\d*/g,'#');
if(skel(x)!==skel(y)) return false;
const nx=nums(x), ny=nums(y); if(nx.length!==ny.length) return false;
return nx.every((v,i)=>Math.abs(v-ny[i])<=Math.max(1e-9, Math.abs(v)*1e-6));
}
function renderCoding(){
const box=$('#codeBox'); if(!box) return; const l=LESSONS[cur], c=l.coding; if(!c){ box.innerHTML=''; return;}
const doneC=(store.codeDone||[]).includes(l.gi);
box.innerHTML=`
<div class="code-task"><b>动手题 ·</b> ${esc(c.task)}</div>
<div class="editor"><div class="cb-bar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span><span class="fn">exercise.py</span><span style="margin-left:auto" class="score" id="codeState">${doneC?'✓ 已通过判定':'尚未通过判定'}</span></div>
<div class="ed-wrap"><div class="ed-gutter" id="edGutter"></div><textarea id="edCode" spellcheck="false">${esc(codeCache[l.gi]!=null? codeCache[l.gi]: c.starter)}</textarea></div></div>
<div class="quiz-foot">
<button class="btn btn-gold" id="runJudge" style="padding:12px 28px;font-size:14.5px">▶ 运行并判定</button>
<button class="btn btn-ghost" id="resetCode" style="padding:12px 22px;font-size:14px">重置代码</button>
<span class="score">代码会在你的浏览器里真的运行，再逐行和标准输出对比，错在哪一行直接标出来。首次运行需联网加载 Python 环境。</span>
</div>
<div class="code-fb" id="codeFb"></div>`;
const ta=$('#edCode'), gut=$('#edGutter');
const syncGutter=(errLine)=>{ const n=ta.value.split('\n').length;
gut.innerHTML=Array.from({length:n},(_,k)=>`<div class="${errLine===k+1?'err-line':''}">${k+1}</div>`).join(''); gut.scrollTop=ta.scrollTop;};
codeCache[l.gi]=ta.value;
ta.addEventListener('input',()=>{ syncGutter(0); codeCache[l.gi]=ta.value;});
ta.addEventListener('scroll',()=>{ gut.scrollTop=ta.scrollTop;});
ta.addEventListener('keydown',e=>{ if(e.key==='Tab'){ e.preventDefault(); ta.setRangeText(' ',ta.selectionStart,ta.selectionEnd,'end'); ta.dispatchEvent(new Event('input'));}});
syncGutter(0);
$('#resetCode').onclick=()=>{ ta.value=c.starter; codeCache[l.gi]=c.starter; const fb=$('#codeFb'); fb.className='code-fb'; fb.innerHTML=''; syncGutter(0);};
$('#runJudge').onclick=()=>judgeCode(syncGutter);
}
async function judgeCode(syncGutter){
const l=LESSONS[cur], c=l.coding, fb=$('#codeFb'), btn=$('#runJudge');
const code=$('#edCode').value;
const cold=!pyWarm;
btn.disabled=true; btn.textContent=cold?'正在准备 Python 环境（首次需联网下载，请稍候）…':'判定中…';
fb.className='code-fb show'; fb.innerHTML=cold?'<span class="fb-t">正在加载 Python 环境…</span><div style="margin-top:6px;color:var(--muted);font-size:13.5px">第一次运行要先联网下载运行环境（约十几 MB，看网络），之后每次判定只要几秒。请不要关掉页面。</div>':'<span class="fb-t">运行中…</span>';
const ime=scanIME(code);
if(ime){ btn.disabled=false; btn.textContent='▶ 运行并判定'; lastJudge[l.gi]='还没运行就被拦下：第 '+ime.line+' 行有中文输入法的全角符号「'+ime.ch+'」，要换成半角「'+ime.half+'」'; showIMEDiag(fb, ime); syncGutter(ime.line); return;}
const files={}; (c.files||[]).forEach(f=>{ if(f==='meals.csv') files[f]=MEALS_CSV; if(f==='ledger.csv') files[f]=LEDGER_CSV;});
let res;
try{ res=await runStudentCode(code, c.pkgs||[], files, c.checkFile||null);}
catch(e){ fb.className='code-fb show fail'; fb.innerHTML='<div class="fb-t">运行环境加载失败</div>多半是网络问题（判定环境需要联网从 CDN 加载）。检查网络后刷新页面再试一次；课文、选择题和演示不受影响。'; btn.disabled=false; btn.textContent='▶ 运行并判定'; return;}
pyWarm=true; btn.disabled=false; btn.textContent='▶ 运行并判定';
if(!res.ok){ lastJudge[l.gi]='运行报错：'+String(res.error||'').split('\n').filter(Boolean).slice(-1)[0].slice(0,140); showCodeError(fb, code, res.error); syncGutter(errLineOf(res.error)); return;}
syncGutter(0);
const act=(res.out||[]).join('\n').split('\n').map(s=>s.replace(/\s+$/,''));
while(act.length&&act[act.length-1]==='') act.pop();
const exp=c.expected.map(s=>String(s).replace(/\s+$/,''));
let ai=0, firstMissing=-1; const rows=[];
for(let ei=0; ei<exp.length; ei++){ let found=false;
while(ai<act.length){ if(judgeEq(exp[ei], act[ai])){ found=true; ai++; break;} ai++;}
if(!found){ firstMissing=ei; rows.push({e:exp[ei], ok:false}); for(let k=ei+1;k<exp.length;k++) rows.push({e:exp[k], ok:false}); break;}
rows.push({e:exp[ei], ok:true});}
let fileOk=true; if(c.checkFile){ fileOk=!!res.fileExists;}
if(firstMissing<0&&fileOk){
lastJudge[l.gi]='判定通过：代码没有报错，期望的内容都出现了';
if(!(store.codeDone||[]).includes(l.gi)){ store.codeDone=store.codeDone||[]; store.codeDone.push(l.gi); save();}
const cs=$('#codeState'); if(cs) cs.textContent='✓ 已通过判定';
fb.className='code-fb show pass';
fb.innerHTML=`<div class="fb-t">✓ 通过！</div>代码没有报错，期望的内容都出现了${act.length>exp.length?'（你多打印的行不扣分）':''}${c.checkFile?'，要求生成的文件也成功生成了':''}。这一课的动手题通过判定。`;
updateProgress(); confettiBurst(); return;
}
fb.className='code-fb show fail';
lastJudge[l.gi]= firstMissing>=0? ('判定未通过：期望的第 '+(firstMissing+1)+' 行内容「'+exp[firstMissing]+'」没有在他的输出里出现，他的输出是「'+act.join(' / ')+'」'): '判定未通过：输出内容对了，但要求生成的文件没有生成';
let head;
if(firstMissing>=0){ head=`期望的第 ${firstMissing+1} 行内容没有在你的输出里出现（多打印的行没关系，缺了期望内容不行）。检查一下是不是少算了、少打印了，或者数字不对。`;
const skel=s=>normBase(s).replace(/-?\d+\.?\d*/g,'#').replace(/\s+/g,'');
const sib=act.find(a=>skel(a)===skel(exp[firstMissing]));
if(sib) head+=`<br>看起来你有一行结构是对的：「${esc(sib)}」，但数字和期望的「${esc(exp[firstMissing])}」不一样——多半是算错了，检查计算过程（有没有漏加一笔、数值用错）。`;}
else head='输出内容都对，但要求生成的文件没有生成——检查保存文件那一行有没有写对、顺序是不是先建好再保存。';
fb.innerHTML=`<div class="fb-t">✗ 还差一点</div><div>${head}</div>
<table><tr><th>期望出现的内容</th><th style="width:76px">状态</th></tr>
${rows.map(r=>`<tr class="${r.ok?'ok':'bad'}"><td>${esc(r.e)}</td><td>${r.ok?'✓ 已出现':'✗ 没出现'}</td></tr>`).join('')}</table>
<div style="margin-top:10px;color:var(--muted);font-size:13px">你的完整输出：</div>
<div class="src-line" style="color:#f0e9d6">${act.length? esc(act.join('\n')): '（没有任何输出）'}</div>`;
}
const FW={'（':'(','）':')','＂':'"','＇':"'",'：':':','；':';','，':',','．':'.','！':'!','？':'?','＝':'=','＋':'+','＜':'<','＞':'>','［':'[','］':']','｛':'{','｝':'}','％':'%','＊':'*','－':'-','＿':'_'};
function scanIME(code){
const lines=code.split('\n'); let inStr=null, triple=false, esc2=false;
for(let li=0; li<lines.length; li++){ const line=lines[li];
for(let ci=0; ci<line.length; ci++){ const ch=line[ci];
if(inStr){ if(esc2){ esc2=false; continue;} if(ch==='\\'){ esc2=true; continue;}
if(triple){ if(line.substr(ci,3)===inStr){ inStr=null; triple=false; ci+=2;} continue;}
if(ch===inStr) inStr=null; continue;}
if(ch==='#') break;
if(ch==='"'||ch==="'"){ const t3=line.substr(ci,3), q3=ch+ch+ch;
if(t3===q3){ inStr=t3; triple=true; ci+=2;} else inStr=ch; continue;}
if(FW[ch]) return {line:li+1, ch, half:FW[ch], src:line};
if(ch==='\u3000') return {line:li+1, ch:'　', half:' ', src:line, space:true};
}
if(!triple) inStr=null;
}
return null;
}
function showIMEDiag(fb, ime){
fb.className='code-fb show fail';
fb.innerHTML=`<div class="fb-t">✗ 第 ${ime.line} 行有个符号是中文输入法打的</div>
<div>「${ime.space?'全角空格':ime.ch}」是<b>全角符号</b>，多半是打代码时输入法没切到英文。Python 只认半角符号，把它换成「${ime.space?'半角空格':ime.half}」再运行。字符串里面的中文标点没问题，指的是代码本身的符号。</div>
<div class="src-line">第 ${ime.line} 行：${esc(ime.src)}</div>`;
}
function lev(a,b){ const dp=[]; for(let i=0;i<=a.length;i++){ dp.push([i]);} for(let j=0;j<=b.length;j++) dp[0][j]=j;
for(let i=1;i<=a.length;i++) for(let j=1;j<=b.length;j++) dp[i][j]=Math.min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+(a[i-1]===b[j-1]?0:1));
return dp[a.length][b.length];}
function suggestName(code, bad){
const names=new Set(); let m;
const pats=[/([A-Za-z_]\w*)\s*=/g, /def\s+([A-Za-z_]\w*)/g, /for\s+([A-Za-z_]\w*)\s+in/g, /import\s+([A-Za-z_]\w*)/g];
pats.forEach(re=>{ while((m=re.exec(code))) names.add(m[1]);});
let best=null, bd=3;
names.forEach(n=>{ const d=lev(bad,n); if(d<bd){ bd=d; best=n;}});
return bd<=2? best: null;
}
function showCodeError(fb, code, errStr){
const line=errLineOf(errStr), raw=String(errStr);
const tm=raw.match(/(SyntaxError|IndentationError|TabError|NameError|TypeError|ValueError|KeyError|IndexError|ZeroDivisionError|FileNotFoundError|ModuleNotFoundError|AttributeError)/);
const type=tm?tm[1]:'Error';
const srcLine=line? (code.split('\n')[line-1]||''): '';
let cause='';
if(/invalid character/.test(raw)){ const cm=raw.match(/invalid character '(.)'/);
cause=`代码里混进了非法字符${cm?'「'+cm[1]+'」':''}——多半是中文输入法打出的全角符号，把它换成半角英文符号再试。`;}
else if(/expected ':'/.test(raw)) cause='这一行末尾漏了冒号「:」——if / else / elif / for / while / def 这些行，最后都要加一个半角冒号。';
else if(/unterminated string|EOL while scanning/.test(raw)) cause='引号没有关上——字符串前后的引号要成对、要是同一种，检查这一行的引号。';
else if(type==='IndentationError'||type==='TabError'){
if(/^\t/.test(srcLine)) cause='这一行开头用了 Tab 缩进，和其他行的空格缩进混在一起了——全篇统一用空格缩进（每层 4 个，或始终 2 个）。';
else if(/unindent does not match/.test(raw)) cause='这一行的缩进和它所属的那一层对不齐——Python 靠缩进分层，同一层的行必须完全对齐。';
else cause='缩进不对：if / for / while / def 的下一行要缩进一层（通常 4 个空格），不该缩进的行不要缩进。';}
else if(type==='NameError'){ const nm=raw.match(/name '([^']+)' is not defined/);
if(nm&&(nm[1]==='pd'||nm[1]==='plt')) cause=`「${nm[1]}」没定义——多半是忘了在最前面先 import（import pandas as pd / import matplotlib.pyplot as plt）。`;
else if(nm){ const cand=suggestName(code, nm[1]);
cause=`名字「${nm[1]}」从来没有定义过。`+(cand?`你是不是想打「${cand}」？对照一下拼写。`:'看看是不是打错字，或者用它之前忘了先赋值（例如先写 '+nm[1]+' =...）。');}
else cause=ERR_ZH.NameError;}
else cause=ERR_ZH[type]||'看看报错信息，对照这一课的讲解再改。';
fb.className='code-fb show fail';
fb.innerHTML=`<div class="fb-t">✗ ${line?`第 ${line} 行出错`:'运行时出错'} · ${type}</div>
<div>${cause}</div>
${srcLine?`<div class="src-line">第 ${line} 行：${esc(srcLine)}</div>`:''}
<div style="margin-top:8px;color:var(--muted);font-size:13px">原始报错：${esc(String(errStr).split('\n').filter(s=>s.trim()).slice(-1)[0]||'')}</div>`;
}
/* ---------- AI tutor (config lives on the Settings view) ---------- */
const PRESETS=[['OpenAI','https://api.openai.com/v1','gpt-4o-mini'],['DeepSeek','https://api.deepseek.com/v1','deepseek-chat'],['通义千问（兼容模式）','https://dashscope.aliyuncs.com/compatible-mode/v1','qwen-plus'],['Moonshot · Kimi','https://api.moonshot.cn/v1','moonshot-v1-8k'],['智谱 GLM','https://open.bigmodel.cn/api/paas/v4','glm-4-flash'],['硅基流动','https://api.siliconflow.com/v1','deepseek-ai/DeepSeek-V3'],['自定义','','']];
let aiCfg=loadJSON(LS_AI, null);
function aiReady(){ return!!(aiCfg&&aiCfg.key&&aiCfg.base&&aiCfg.model);}
function fillSettings(){
const sel=$('#aiPreset'); if(!sel) return;
sel.innerHTML=PRESETS.map((p,i)=>`<option value="${i}">${p[0]}</option>`).join('');
if(aiCfg){ $('#aiBase').value=aiCfg.base||''; $('#aiKey').value=aiCfg.key||''; $('#aiModel').value=aiCfg.model||'';
const pi=PRESETS.findIndex(p=>p[1]&&p[1]===aiCfg.base); sel.value=pi>=0? pi: PRESETS.length-1;}
else { sel.value=0; $('#aiBase').value=PRESETS[0][1]; $('#aiModel').value=PRESETS[0][2]; $('#aiKey').value='';}
$('#aiState').textContent=aiReady()? ('已接入 · '+aiCfg.model+'（Key 只存在本机浏览器）'): '尚未保存 Key';
}
$('#aiPreset').addEventListener('change',e=>{ const p=PRESETS[+e.target.value]; if(p[1]) $('#aiBase').value=p[1]; if(p[2]) $('#aiModel').value=p[2];});
$('#aiSave').onclick=()=>{
aiCfg={base:$('#aiBase').value.trim().replace(/\/+$/,''), key:$('#aiKey').value.trim(), model:$('#aiModel').value.trim()};
if(!aiReady()){ $('#aiState').textContent='三项都要填：接口地址、Key、模型名'; return;}
try{ localStorage.setItem(LS_AI, JSON.stringify(aiCfg));}catch(e){}
$('#aiState').textContent='已保存 · '+aiCfg.model+'（Key 只存在本机浏览器，不会上传）';
if(cur>=0) renderAiBox();
};
$('#aiClear').onclick=()=>{ try{ localStorage.removeItem(LS_AI);}catch(e){} aiCfg=null; $('#aiKey').value=''; $('#aiState').textContent='已清除'; if(cur>=0) renderAiBox();};
$('#wipeBtn').onclick=()=>{ [LS_MAIN,LS_PREF,LS_CHATS].forEach(k=>{ try{ localStorage.removeItem(k);}catch(e){}});
store.done=[]; store.best={}; store.codeDone=[]; store.answers={}; doneSet.clear();
$('#wipeState').textContent='已清除，进度从零开始'; updateProgress();};
let aiChats=loadJSON(LS_CHATS, {});
function saveChats(){ try{ localStorage.setItem(LS_CHATS, JSON.stringify(aiChats));}catch(e){}}
function chatOf(gi){ if(!aiChats[gi]) aiChats[gi]=[]; return aiChats[gi];}
function fmtAi(t){ return esc(t).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/`([^`\n]+)`/g,'<code>$1</code>');}
function bubbleHtml(m){ return m.role==='user'? `<div class="msg u">${esc(m.content)}</div>`: `<div class="msg a">${fmtAi(m.content)}</div>`;}
function renderAiBox(){
const box=$('#aiBox'); if(!box) return;
if(!aiReady()){
box.innerHTML=`<div class="why show">想问更深、或者想要一个生活化的讲解？可以接入你自己的 AI，在这一课里直接向它提问、连续追问。<br>本站不提供 AI 服务：到「设置」页填入你自己的 API Key 即可使用；Key 只保存在你本机浏览器里，不会上传。不配置也完全不影响学习。</div>
<div class="quiz-foot"><button class="btn btn-gold" id="aiGoSet" style="padding:11px 26px;font-size:14px">去设置页填 Key</button></div>`;
$('#aiGoSet').onclick=()=>showView('settings'); return;
}
const l=LESSONS[cur], chat=chatOf(l.gi);
box.innerHTML=`
<div class="ai-thread" id="aiThread">${chat.length? chat.map(m=>bubbleHtml(m)).join(''): '<div class="msg a">我是这一课的 AI 导师。你在这一课选错的题、写过的代码和判定结果我都看得到，可以针对你卡住的地方讲；也能连续追问，回答时你可以随时打断。</div>'}</div>
<div class="ai-qrow"><input id="aiQ" type="text" placeholder="接着问…（Enter 发送）"><button class="btn btn-gold" id="aiAsk" style="padding:11px 22px;font-size:14px">发送</button></div>
<div class="quiz-foot" style="margin-top:10px"><button class="btn btn-ghost" id="aiExplain" style="padding:9px 20px;font-size:13px">让 AI 讲解这一课</button><button class="btn btn-ghost" id="aiStop" style="padding:9px 20px;font-size:13px;display:none">停止生成</button><button class="btn btn-ghost" id="aiReset" style="padding:9px 20px;font-size:13px">清空对话</button><span class="score">当前模型 · ${esc(aiCfg.model)} · AI 看得到你的作答</span></div>`;
const th=$('#aiThread'); th.scrollTop=th.scrollHeight;
const send=()=>{ const v=$('#aiQ').value.trim(); if(v){ $('#aiQ').value=''; askAI(v);}};
$('#aiAsk').onclick=send;
$('#aiQ').addEventListener('keydown',e=>{ if(e.key==='Enter') send();});
$('#aiExplain').onclick=()=>askAI('请讲解这一课的核心概念，配一个生活化的例子，再提醒一个最容易踩的坑。');
$('#aiStop').onclick=()=>{ if(aiAbort) aiAbort.abort();};
$('#aiReset').onclick=()=>{ if(aiAbort) aiAbort.abort(); aiChats[l.gi]=[]; saveChats(); renderAiBox();};
}
function attemptContext(l){
const parts=[];
(l.quiz||[]).forEach((q,qi)=>{ const a=store.answers[l.gi+'-'+qi];
if(a!==undefined&&a!==null) parts.push('选择题'+(qi+1)+'：'+q.q+'\n他的选择：'+q.opts[a]+'（'+(a===q.ans?'答对了':'答错了')+'）\n正确答案：'+q.opts[q.ans]+(q.why?'；解析：'+q.why:''));});
if(l.coding){ const code=codeCache[l.gi], j=lastJudge[l.gi];
if(code) parts.push('动手题：'+l.coding.task+'\n他最近写的代码：\n'+code+(j?'\n最近一次判定：'+j:''));
else if(j) parts.push('动手题最近一次判定：'+j);}
return parts.length? '\n'+parts.join('\n\n'): '';
}
let aiAbort=null, aiSeq=0;
async function askAI(q){
const l=LESSONS[cur], chat=chatOf(l.gi), th=$('#aiThread'); if(!th) return;
if(aiAbort) aiAbort.abort();
const mySeq=++aiSeq;
chat.push({role:'user', content:q}); if(chat.length>40) chat.splice(0, chat.length-40); saveChats();
th.insertAdjacentHTML('beforeend', bubbleHtml({role:'user',content:q}));
const bub=document.createElement('div'); bub.className='msg a'; bub.textContent='思考中…'; th.appendChild(bub);
th.scrollTop=th.scrollHeight;
const stopBtn=$('#aiStop'); if(stopBtn) stopBtn.style.display='';
const sys='你是一位耐心的 Python 编程老师，正在辅导一位自学 Python 的初学者。用简体中文、通俗易懂地讲解，多用生活例子（记账、金额、问卷）。如果学生问的是练习题，不要直接给答案，只给提示和思路，引导他自己想出来。结合之前的对话回答追问。回答控制在 300 字以内，分段清晰。';
const ctx='当前课程：第 '+(l.gi+1)+' 课《'+l.title+'》\n讲解：'+dispExplain(l)+'\n注意点：'+l.tip+'\n示例代码：\n'+l.code+'\n运行结果：'+l.out.join(' / ');
const att=attemptContext(l);
const hist=chat.slice(-12);
const msgs=[{role:'system',content:sys}];
if(att) msgs.push({role:'system',content:att});
hist.forEach((m,i)=>{ msgs.push({role:m.role, content:(i===0&&m.role==='user')? ctx+'\n\n学生的问题：'+m.content: m.content});});
const ctrl=new AbortController(); aiAbort=ctrl;
let acc='', settled=false;
try{
const r=await fetch(aiCfg.base+'/chat/completions',{method:'POST', signal:ctrl.signal,
headers:{'Content-Type':'application/json','Authorization':'Bearer '+aiCfg.key},
body:JSON.stringify({model:aiCfg.model,temperature:0.7,stream:true,messages:msgs})});
if(!r.ok){ const j=await r.json().catch(()=>null); throw new Error('请求失败：'+((j&&j.error&&j.error.message)||('HTTP '+r.status))+'。请到设置页检查接口地址、Key 和模型名。');}
const ct=(r.headers.get('content-type')||'');
if(ct.includes('text/event-stream')&&r.body&&r.body.getReader){
const reader=r.body.getReader(), dec=new TextDecoder(); let buf='';
while(true){ const rd=await reader.read(); if(rd.done) break;
buf+=dec.decode(rd.value,{stream:true});
let idx; while((idx=buf.indexOf('\n'))>=0){ const line=buf.slice(0,idx).trim(); buf=buf.slice(idx+1);
if(line.startsWith('data:')){ const data=line.slice(5).trim();
if(data&&data!=='[DONE]'){ try{ const jj=JSON.parse(data); const delta=jj.choices&&jj.choices[0]&&jj.choices[0].delta&&jj.choices[0].delta.content;
if(delta){ acc+=delta; if(mySeq===aiSeq){ bub.innerHTML=fmtAi(acc); th.scrollTop=th.scrollHeight;}}}catch(e){}}}}
}
} else { const j=await r.json(); const t=j&&j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content; if(t) acc=t;}
settled=true;
}catch(err){
if(err&&err.name==='AbortError'){ if(acc){ acc+='\n\n（已被打断）'; settled=true;} else if(mySeq===aiSeq){ bub.textContent='（已停止生成）';}}
else { if(mySeq===aiSeq){ bub.classList.add('err'); bub.textContent=(err&&err.message?err.message:'请求没有发出去：可能是网络问题，或者该接口不允许浏览器直接调用（跨域限制）。')+'这条不计入对话，可以直接重发。';} chat.pop(); saveChats();}
}
if(settled&&acc){ chat.push({role:'assistant', content:acc}); saveChats(); if(mySeq===aiSeq) bub.innerHTML=fmtAi(acc);}
if(mySeq===aiSeq){ aiAbort=null; if(stopBtn) stopBtn.style.display='none'; th.scrollTop=th.scrollHeight;}
}
/* ---------- search & misc wiring ---------- */
$('#searchBox').addEventListener('input',e=>{
const kw=e.target.value.trim(); let any=false;
$$('.stage').forEach(sec=>{ let vis=false;
sec.querySelectorAll('.lrow').forEach(n=>{ const hit=!kw||n.dataset.title.includes(kw); n.style.display=hit?'':'none'; if(hit){ vis=true; any=true;}});
sec.style.display=vis?'':'none';});
$('#emptyMsg').style.display=any?'none':'block';
});
$('#ctaStart').onclick=()=>{ openLesson(firstOpen());};
$('#ctaRoute').onclick=()=>document.getElementById('route').scrollIntoView({behavior:reduced?'auto':'smooth'});
$('#pcGo').onclick=()=>{ openLesson(firstOpen());};
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&curView==='lesson') showView('home');});
renderRoute(); observeReveals(); heroLoop();
</script>
<script>
/* ---------- detailed explanations: same wording swap as the website edition ---------- */
const MAJOR_PAIRS=[['个人账本年度报告','个人数据年度报告'],['账本年度报告','数据年度报告'],['账本报告','数据报告'],['会计应用','数据应用'],['把账本数据玩起来','把真实数据玩起来'],['账本','记录']];
function swapMajor(t){ if(curMode!=='general'||!t) return t; let s=t; for(const pr of MAJOR_PAIRS) s=s.split(pr[0]).join(pr[1]); return s; }
function dispExplain(l){ return swapMajor(l.explain||l.intro); }
/* ---------- major switch: accounting (default) / general — release edition only ----------
   Only scene wording changes (stage name, lesson titles/intros/tips for the
   accounting-flavoured lessons). Code, datasets, expected outputs and judging
   are never touched, so judging results are identical in both modes. */
const LS_MODE='pytut-space-mode';
const MODE_OV={
  stageName:{2:'数据应用'},
  stageSub:{2:'用 pandas 把表格数据玩起来'},
  lessons:{
    26:{intro:'pandas 是处理表格的神器：read_csv 一行把 CSV 读成表，df["金额"] 取一整列，.sum() 直接加总——数据统计一步到位。'},
    29:{title:'综合项目：数据报告',
        intro:'终点站：读一份消费记录表、算总支出、找最贵一笔——pandas 三行做出一份数据报告。学完这一课，整条路线就走通了。',
        tip:'数据报告最常用就是 sum 求和、max 找最大一笔。'},
    35:{title:'综合项目：个人数据年度报告',
        intro:'把这一阶段学的东西串起来：读入一整年的消费记录 ledger.csv（月份、类别、金额），按月汇总、找最高月份和最高类别，最后拼出一份像样的报告。真实数据就是把行数换成几百行，代码一行都不用改。'}
  }
};
const BASE_STAGES=JSON.parse(JSON.stringify(STAGES));
const BASE_LESSONS=JSON.parse(JSON.stringify(LESSONS.map(l=>({title:l.title, intro:l.intro, tip:l.tip}))));
let curMode='accounting';
try{ const m=localStorage.getItem(LS_MODE); if(m==='general'||m==='accounting') curMode=m; }catch(e){}
function applyMode(m){
  curMode=m;
  STAGES.forEach((st,si)=>{ st.name=BASE_STAGES[si].name; st.sub=BASE_STAGES[si].sub;
    if(m==='general'){ if(MODE_OV.stageName[si]) st.name=MODE_OV.stageName[si]; if(MODE_OV.stageSub[si]) st.sub=MODE_OV.stageSub[si]; } });
  LESSONS.forEach((l,i)=>{ const b=BASE_LESSONS[i]; l.title=b.title; l.intro=b.intro; l.tip=b.tip;
    if(m==='general'&&MODE_OV.lessons[i]){ const o=MODE_OV.lessons[i]; if(o.title) l.title=o.title; if(o.intro) l.intro=o.intro; if(o.tip) l.tip=o.tip; } });
  const hr=$('#heroReport'); if(hr) hr.textContent=(m==='general'?'数据报告':'账本报告');
  const ss=$('#statsStages'); if(ss) ss.textContent=STAGES.map(s=>s.name).join(' · ');
  $$('.segctl').forEach(seg=>{ seg.querySelectorAll('button').forEach(b=>b.classList.toggle('on', b.dataset.mode===m)); });
  const ms=$('#modeState'); if(ms) ms.textContent='当前：'+(m==='general'?'通用方向':'会计方向');
  renderRoute();
  if(curView==='lesson'&&cur>=0) openLesson(cur);
}
function setMode(m, saveIt){ if(saveIt!==false){ try{ localStorage.setItem(LS_MODE, m); }catch(e){} } applyMode(m); }
$$('.segctl').forEach(seg=>{ seg.querySelectorAll('button').forEach(b=>{ b.onclick=()=>setMode(b.dataset.mode); }); });
(function initMode(){
  let seen=false; try{ seen=!!localStorage.getItem(LS_MODE); }catch(e){}
  if(curMode==='general') applyMode('general'); else applyMode('accounting');
  if(!seen){ const mm=$('#modeModal'); if(mm){ mm.classList.add('open');
    mm.querySelectorAll('[data-pick]').forEach(b=>{ b.onclick=()=>{ setMode(b.dataset.pick); mm.classList.remove('open'); }; });
    const sk=$('#modeSkip'); if(sk) sk.onclick=()=>{ setMode('accounting'); mm.classList.remove('open'); };
  } }
})();
</script>
</body>
</html>
"""


def main():
    mod = load_source()
    data = build_data(mod)
    stages = sanitize(mod.STAGES)
    meals = mod.MEALS_CSV
    ledger = mod.LEDGER_CSV
    assert len(data) == 41, f"expected 41 lessons, got {len(data)}"
    html = TEMPLATE.replace("__STAGES_JSON__", json.dumps(stages, ensure_ascii=False))
    html = html.replace("__LESSONS_JSON__", json.dumps(data, ensure_ascii=False))
    html = html.replace("__MEALS_JSON__", json.dumps(meals, ensure_ascii=False))
    html = html.replace("__LEDGER_JSON__", json.dumps(ledger, ensure_ascii=False))
    for bad in FORBIDDEN:
        assert bad not in html, f"forbidden identifier leaked into output: {bad}"
    assert GENERIC_NAME in html, "generic example name missing - sanitisation did not run?"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("written", OUT, len(html.encode("utf-8")), "bytes;",
          len(data), "lessons;",
          sum(len(x["quiz"]) for x in data), "quiz questions;",
          sum(1 for x in data if "coding" in x), "coding tasks;",
          sum(x["mins"] for x in data), "minutes")


if __name__ == "__main__":
    main()
