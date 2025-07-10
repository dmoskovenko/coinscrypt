#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, json, getopt, curses

# Python 2/3 urllib
import sys
if sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.error import URLError
else:
    from urllib2 import urlopen, URLError

API_URL = (
    "https://api.coingecko.com/api/v3/coins/markets"
    "?vs_currency=usd&order=market_cap_desc"
    "&per_page=100&sparkline=false"
    "&price_change_percentage=1h%2C24h%2C7d&page=1"
)

HEADER_LINES = 3
FOOTER_LINES = 2
SCROLL_INTERVAL = 30  # seconds
MIN_COL_WIDTH = 4     # for ellipsis
GAP = 2               # spaces between columns


def parse_args():
    opts, args = getopt.getopt(sys.argv[1:], 'ut:n', ['update', 'top=', 'name'])
    update = False; show_name = False; top = 0
    for o, a in opts:
        if o in ('-u','--update'): update = True
        elif o in ('-n','--name'): show_name = True
        elif o in ('-t','--top') and a.isdigit(): top = int(a)
    tickers = [a.upper() for a in args]
    return update, top, show_name, tickers


def fetch_data(retries=10, delay=5):
    for i in range(retries):
        try:
            resp = urlopen(API_URL, timeout=5)
            data = resp.read()
            if isinstance(data, bytes): data = data.decode()
            return json.loads(data)
        except URLError:
            if i < retries - 1: time.sleep(delay)
            else: sys.exit("Connection error")


def build_records(raw, tickers, top, show_name):
    recs = []
    for e in raw:
        rank = e.get('market_cap_rank')
        sym = e.get('symbol','').upper()
        name = e.get('name','')
        if ((top and rank is not None and rank <= top) or (sym in tickers)):
            def fmt(p): return '{:+.2%}'.format(p/100) if p is not None else '   N/A   '
            v1 = e.get('price_change_percentage_1h_in_currency')
            v24 = e.get('price_change_percentage_24h')
            v7 = e.get('price_change_percentage_7d_in_currency')
            rec = [str(rank) if rank is not None else 'N/A', sym]
            if show_name: rec.append(name)
            rec += [
                '{:.2f}'.format(e.get('current_price',0)),
                fmt(v1), fmt(v24), fmt(v7),
                '{:,.0f}'.format(e.get('total_volume',0)),
                '{:,.0f}'.format(e.get('market_cap',0))
            ]
            raw_vals = {'1h':v1,'24h':v24,'7d':v7}
            recs.append((rec, raw_vals))
    return recs


def curses_main(stdscr, update, top, show_name, tickers):
    # init colors
    curses.start_color(); curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED,-1)
    curses.init_pair(2, curses.COLOR_GREEN,-1)
    curses.init_pair(3, curses.COLOR_WHITE,-1)
    col_red = curses.color_pair(1)
    col_grn = curses.color_pair(2)
    col_gray = curses.color_pair(3)|curses.A_DIM
    col_norm = curses.A_NORMAL

    curses.curs_set(0); stdscr.keypad(True); stdscr.timeout(100)

    records=[]; last_fetch=0; v_off=0; h_off=0
    while True:
        h,w=stdscr.getmaxyx(); now=time.time()
        if not records or (update and now-last_fetch>=SCROLL_INTERVAL):
            raw=fetch_data(); records=build_records(raw,tickers,top,show_name)
            last_fetch=now; v_off=0; h_off=0

        # prepare columns
        cols=['Rank','Ticker']
        if show_name: cols.append('Name')
        cols+=['Price','1h','24h','7d','Vol24h','MktCap']
        col_count=len(cols)
        # compute max content widths
        max_w=[len(c) for c in cols]
        for rec,_ in records:
            for i,cell in enumerate(rec):
                L=len(str(cell)); max_w[i]=max(max_w[i],L)
        # total required width including gaps
        total_req=sum(max_w)+GAP*(col_count-1)
        ell_idx=None
        if total_req> w:
            diff=total_req-w
            # find widest column to shrink
            idx=max(range(col_count), key=lambda i:max_w[i])
            neww=max(MIN_COL_WIDTH, max_w[idx]-diff)
            if neww<max_w[idx]: max_w[idx]=neww; ell_idx=idx
            total_req=sum(max_w)+GAP*(col_count-1)
        # separator line full width
        sep_full='─'*w
        stdscr.erase()
        # draw header sep
        stdscr.addstr(0,0,sep_full,col_gray)
        # header titles
        x=0
        for i,title in enumerate(cols):
            wcol=max_w[i]; text=title.ljust(wcol)
            if x-h_off< w and x+wcol-h_off>0:
                sub=text[max(0,h_off-x):][:min(wcol,w,x+wcol-h_off)]
                try: stdscr.addstr(1,max(0,x-h_off),sub,col_gray)
                except: pass
            x+=wcol+GAP
        # underline
        stdscr.addstr(2,0,sep_full,col_gray)

        # body rows
        view_h=max(0,h-HEADER_LINES-FOOTER_LINES)
        max_v_off=max(0,len(records)-view_h)
        for r in range(view_h):
            if v_off+r>=len(records): break
            rec,rawv=records[v_off+r]; y=HEADER_LINES+r; x=0
            for i,cell in enumerate(rec):
                wcol=max_w[i]; s=str(cell)
                if ell_idx==i and len(s)>wcol: s=s[:wcol-3]+'...'
                else: s=s.ljust(wcol)
                if x-h_off< w and x+wcol-h_off>0:
                    sub=s[max(0,h_off-x):][:min(wcol,w,x+wcol-h_off)]
                    if cols[i] in ('1h','24h','7d'):
                        rv=rawv[cols[i]]; attr=col_grn if rv and rv>=0 else col_red if rv else col_norm
                    else: attr=col_norm
                    try: stdscr.addstr(y,max(0,x-h_off),sub,attr)
                    except: pass
                x+=wcol+GAP
        # footer sep
        row_s=HEADER_LINES+view_h; row_f=row_s+1
        if row_s<h: stdscr.addstr(row_s,0,sep_full,col_gray)
        # footer time
        if row_f<h:
            ft='Updated: '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(last_fetch))
            stdscr.addstr(row_f,0,ft[:w],col_gray)
        stdscr.refresh()

        # input handling
        key=stdscr.getch()
        if key in (ord('q'),ord('Q')): break
        if key in (curses.KEY_DOWN,ord('j')) and v_off<max_v_off: v_off+=1
        if key in (curses.KEY_UP,ord('k')) and v_off>0: v_off-=1
        if key in (curses.KEY_RIGHT,ord('l')) and h_off<max(0,total_req-w): h_off+=1
        if key in (curses.KEY_LEFT,ord('h')) and h_off>0: h_off-=1
        if key == curses.KEY_RESIZE:
            # on resize, just redraw without refetching data
            continue


def main():
    update,top,show_name,tickers=parse_args()
    curses.wrapper(curses_main,update,top,show_name,tickers)

if __name__=='__main__': main()
