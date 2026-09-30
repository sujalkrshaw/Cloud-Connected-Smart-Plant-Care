export default function LineChart({data,keyName,color='currentColor',unit=''}){
 if(!data?.length)return <div className="empty-chart">Waiting for sensor history…</div>
 const w=700,h=220,p=28,vals=data.map(x=>Number(x[keyName]||0)),min=Math.min(...vals),max=Math.max(...vals),range=max-min||1
 const points=vals.map((v,i)=>`${p+i*(w-2*p)/Math.max(1,vals.length-1)},${h-p-(v-min)*(h-2*p)/range}`).join(' ')
 return <svg viewBox={`0 0 ${w} ${h}`} className="chart"><line x1={p} y1={h-p} x2={w-p} y2={h-p} className="axis"/><polyline points={points} fill="none" stroke={color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>{vals.slice(-1).map((v,i)=><text key={i} x={w-p} y={30} className="chart-label">{v.toFixed(1)}{unit}</text>)}</svg>
}
