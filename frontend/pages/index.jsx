import { useState } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'

export default function Home(){
  const [prompt,setPrompt] = useState('')
  const [reply,setReply] = useState('')
  const [loading,setLoading] = useState(false)

  async function sendChat(){
    if(!prompt) return
    setLoading(true)
    setReply('')
    try{
      const res = await axios.post(process.env.NEXT_PUBLIC_BACKEND_URL + '/api/chat', {messages:[{role:'user',content:prompt}]})
      const content = res.data.reply?.content || JSON.stringify(res.data.reply)
      setReply(content)
    }catch(e){
      setReply('Erreur: ' + (e.response?.data?.detail || e.message))
    }finally{setLoading(false)}
  }

  return (
    <main className=\"min-h-screen flex items-center justify-center p-8\">
      <div className=\"max-w-3xl w-full\">
        <motion.h1 className=\"text-4xl font-bold neon-title mb-6\" initial={{opacity:0,y:-20}} animate={{opacity:1,y:0}}>Nexus — IA Multimodale</motion.h1>

        <motion.div className=\"bg-white/5 p-6 rounded-2xl shadow-2xl\" whileHover={{scale:1.01}}>
          <textarea value={prompt} onChange={e=>setPrompt(e.target.value)} rows={4} placeholder=\"Demande, décris une image, envoie un audio...\" className=\"w-full p-4 rounded-md bg-transparent outline-none resize-y\" />
          <div className=\"flex gap-3 mt-4\">
            <button onClick={sendChat} className=\"px-6 py-2 rounded-full border border-white/20 hover:bg-white/5\">{loading? '...' : 'Envoyer'}</button>
          </div>

          <div className=\"mt-6 p-4 bg-black/50 rounded\">
            <h3 className=\"text-sm text-slate-300\">Réponse</h3>
            <pre className=\"whitespace-pre-wrap\">{reply}</pre>
          </div>
        </motion.div>
      </div>
    </main>
  )
}
