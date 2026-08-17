"""Momentum-projected correlators on an L=8 D_4 torus: the three behaviours."""
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")
L=8; C=np.load("rows.npy"); M=[tuple(int(y) for y in x) for x in np.load("moms.npy")]
def get(m):
    if tuple(m) in M: return C[M.index(tuple(m))], 1
    pm=tuple((x+4)%8 for x in m); return C[M.index(pm)]*np.array([(-1)**t for t in range(L)]), -1
cases=[((0,0,4), r"$p=(0,0,\pi)$", r"$\sum_i\cos p_i=+1$", "#0072B2"),
       ((4,4,0), r"$p=(\pi,\pi,0)$", r"$\sum_i\cos p_i=-1$", "#D55E00"),
       ((2,2,2), r"$p=\frac{\pi}{2}(1,1,1)$", r"$\sum_i\cos p_i=0$", "#009E73")]
fig,axes=plt.subplots(1,2,figsize=(7.2,3.2))
ax=axes[0]
for j,(m,lab,sub,col) in enumerate(cases):
    c,_=get(m); t=np.arange(6); c=c[:6]
    y=np.abs(c); nz=y>1e-12*abs(c[0])
    ls="-" if j!=1 else "--"
    ax.plot(t[nz],y[nz],ls,color=col,lw=1.2,zorder=2+j)
    pos=nz&(c>0); neg=nz&(c<0)
    ax.plot(t[pos],y[pos],"o",color=col,ms=5.5,mec="white",mew=0.7,zorder=5)
    ax.plot(t[neg],y[neg],"v",color=col,ms=7.0,mfc="white",mew=1.3,zorder=5)
    if (~nz).any(): ax.plot(t[~nz],np.full((~nz).sum(),3e-11),"x",color=col,ms=7,mew=1.6,zorder=5)
ax.set_yscale("log"); ax.set_ylim(3e-12,6e-2); ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$|C_\pi(t,\vec p\,)|$")
ax.set_title(r"(a) $L=8$ $D_4$: three behaviours", fontsize=9.6)
ax.text(0.10,1.1e-4,r"$(0,0,\pi)$",color="#0072B2",fontsize=8.6)
ax.text(2.6,1.2e-6,r"$(\pi,\pi,0)$ (same $|C|$)",color="#D55E00",fontsize=8.6)
ax.text(3.35,2.0e-8,r"$\frac{\pi}{2}(1,1,1)$",color="#009E73",fontsize=8.6)
ax.text(0.10,7e-12,r"filled $=C>0$,  open $\bigtriangledown = C<0$,  $\times$ $= C\equiv 0$",
        fontsize=7.6,color="#444444")
ax=axes[1]
import itertools
mm=[m for m in itertools.product(range(L),repeat=3)]
sc=np.array([sum(np.cos(2*np.pi*x/L) for x in m) for m in mm])
pn=np.array([np.linalg.norm(np.mod(np.array(m)*2*np.pi/L+np.pi,2*np.pi)-np.pi) for m in mm])
for lo,hi,col,lab in ((1e-9,9,"#0072B2","positive"),(-9,-1e-9,"#D55E00","alternating")):
    s=(sc>lo)&(sc<hi); ax.plot(pn[s],sc[s],".",color=col,ms=3.0)
s=np.abs(sc)<1e-9
ax.plot(pn[s],sc[s],"o",color="#009E73",ms=4.5,mec="white",mew=0.5)
ax.axhline(0,color="#888888",lw=0.7)
ax.set_xlabel(r"$|\vec p\,|$"); ax.set_ylabel(r"$\sum_i \cos p_i$")
ax.set_title(r"(b) the sign of the one-step amplitude", fontsize=9.6)
ax.text(0.15,2.3,"positive correlator",color="#0072B2",fontsize=8.4)
ax.text(0.15,-2.6,"alternating (relabel $\\vec p \\to \\vec p+\\pi\\vec 1$)",
        color="#D55E00",fontsize=8.4)
ax.text(2.05,0.30,r"$34/256$: no signal at odd $t$",color="#009E73",fontsize=8.4)
fig.tight_layout(pad=0.5)
fig.savefig("fig-d4-positivity.pdf"); fig.savefig("fig-d4-positivity.png",dpi=200)
print("ok")
