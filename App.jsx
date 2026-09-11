import React, { useState } from 'react';
import { FileText, Plus, Trash2, Printer, Save } from 'lucide-react';

export default function App() {
  const [formData, setFormData] = useState({
    empresa: '',
    cpm: '',
    endereco: '',
    bairro: '',
    cidade: '',
    estado: '',
    solicitante: '',
    departamento: '',
    email: '',
    telefone: '',
    servico: 'Levantamento de Campo',
    servicosExecutar: '',
    area: '',
    horas: Array(7).fill({
      diaSemana: '',
      data: '',
      chegada: '',
      saida: '',
      intervalo: '',
      deslocamentoIda: '',
      deslocamentoVolta: '',
      distanciaIda: '',
      distanciaVolta: ''
    }),
    despesas: {
      pedagio: '',
      refeicao: '',
      hotel: '',
      outros: ''
    }
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleHoraChange = (index, field, value) => {
    const novasHoras = [...formData.horas];
    novasHoras[index] = { ...novasHoras[index], [field]: value };
    setFormData(prev => ({ ...prev, horas: novasHoras }));
  };

  const handleDespesaChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      despesas: { ...prev.despesas, [field]: value }
    }));
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="min-h-screen bg-slate-100 p-4 md:p-8 text-slate-800">
      <div className="max-w-5xl mx-auto bg-white shadow-lg rounded-xl overflow-hidden print:shadow-none">
        
        {/* Cabeçalho */}
        <div className="bg-slate-900 text-white p-6 flex flex-col md:flex-row justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold tracking-wider">KTSA AUTOMAÇÃO INDUSTRIAL</h1>
            <p className="text-sm text-slate-400">Relatório de Serviço de Campo - RSC</p>
          </div>
          <div className="mt-4 md:mt-0 flex gap-2 print:hidden">
            <button 
              onClick={handlePrint}
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-sm font-medium transition"
            >
              <Printer size={16} /> Imprimir / PDF
            </button>
          </div>
        </div>

        {/* Formulário */}
        <div className="p-6 space-y-6">
          
          {/* Dados do Cliente */}
          <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
            <h2 className="text-md font-semibold text-slate-700 mb-3 uppercase tracking-wide">1. Dados do Cliente / Atendimento</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Empresa</label>
                <input 
                  type="text" 
                  value={formData.empresa} 
                  onChange={e => handleChange('empresa', e.target.value)}
                  className="w-full border border-slate-300 rounded p-2 text-sm bg-white"
                  placeholder="Nome do cliente"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Número CPM</label>
                <input 
                  type="text" 
                  value={formData.cpm} 
                  onChange={e => handleChange('cpm', e.target.value)}
                  className="w-full border border-slate-300 rounded p-2 text-sm bg-white"
                  placeholder="Nº CPM"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Solicitante</label>
                <input 
                  type="text" 
                  value={formData.solicitante} 
                  onChange={e => handleChange('solicitante', e.target.value)}
                  className="w-full border border-slate-300 rounded p-2 text-sm bg-white"
                  placeholder="Nome do solicitante"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-xs font-medium text-slate-600 mb-1">Endereço</label>
                <input 
                  type="text" 
                  value={formData.endereco} 
                  onChange={e => handleChange('endereco', e.target.value)}
                  className="w-full border border-slate-300 rounded p-2 text-sm bg-white"
                  placeholder="Endereço completo"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Bairro</label>
                <input 
                  type="text" 
                  value={formData.bairro} 
                  onChange={e => handleChange('bairro', e.target.value)}
                  className="w-full border border-slate-300 rounded p-2 text-sm bg-white"
                  placeholder="Bairro"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Cidade</label>
                <input 
                  type="text" 
                  value={formData.cidade} 
                  onChange={e => handleChange('cidade', e.target.value)}
                  className="w-full border border-slate-300 rounded p-2 text-sm bg-white"
                  placeholder="Cidade"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Estado</label>
                <input 
                  type="text" 
                  value={formData.estado} 
                  onChange={e => handleChange('estado', e.target.value)}
                  className="w-full border border-slate-300 rounded p-2 text-sm bg-white"
                  placeholder="UF"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Telefone / Fax</label>
                <input 
                  type="text" 
                  value={formData.telefone} 
                  onChange={e => handleChange('telefone', e.target.value)}
                  className="w-full border border-slate-300 rounded p-2 text-sm bg-white"
                  placeholder="(00) 0000-0000"
                />
              </div>
            </div>
          </div>

          {/* Tipo de Serviço */}
          <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
            <h2 className="text-md font-semibold text-slate-700 mb-3 uppercase tracking-wide">2. Tipo de Serviço</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {['Levantamento de Campo', 'Assistência Técnica', 'Comissionamento', 'Start-up', 'Operação Assistida', 'Contrato de Manutenção', 'Outro'].map((serv) => (
                <label key={serv} className="flex items-center space-x-2 text-sm cursor-pointer">
                  <input 
                    type="radio" 
                    name="servico" 
                    checked={formData.servico === serv}
                    onChange={() => handleChange('servico', serv)}
                    className="text-blue-600"
                  />
                  <span>{serv}</span>
                </label>
              ))}
            </div>
            <div className="mt-4">
              <label className="block text-xs font-medium text-slate-600 mb-1">Serviços a Executar / Escopo</label>
              <textarea 
                rows="3" 
                value={formData.servicosExecutar} 
                onChange={e => handleChange('servicosExecutar', e.target.value)}
                className="w-full border border-slate-300 rounded p-2 text-sm bg-white"
                placeholder="Descreva os serviços planejados..."
              />
            </div>
          </div>

          {/* Relatório de Horas (Resumo Semanal) */}
          <div className="border border-slate-200 rounded-lg p-4 bg-slate-50 overflow-x-auto">
            <h2 className="text-md font-semibold text-slate-700 mb-3 uppercase tracking-wide">3. Relatório de Horas (Apontamento)</h2>
            <table className="w-full text-xs text-left border-collapse min-w-[700px]">
              <thead>
                <tr className="bg-slate-200 text-slate-700">
                  <th className="p-2 border">Dia</th>
                  <th className="p-2 border">Data</th>
                  <th className="p-2 border">Chegada</th>
                  <th className="p-2 border">Saída</th>
                  <th className="p-2 border">Intervalo</th>
                  <th className="p-2 border">Desloc. Ida</th>
                  <th className="p-2 border">Desloc. Volta</th>
                  <th className="p-2 border">Dist. Ida (Km)</th>
                  <th className="p-2 border">Dist. Volta (Km)</th>
                </tr>
              </thead>
              <tbody>
                {['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'].map((dia, idx) => (
                  <tr key={dia} className="bg-white">
                    <td className="p-2 border font-medium bg-slate-50">{dia}</td>
                    <td className="p-2 border"><input type="text" placeholder="DD/MM" className="w-full border-0 p-1" value={formData.horas[idx]?.data || ''} onChange={e => handleHoraChange(idx, 'data', e.target.value)} /></td>
                    <td className="p-2 border"><input type="text" placeholder="00:00" className="w-full border-0 p-1" value={formData.horas[idx]?.chegada || ''} onChange={e => handleHoraChange(idx, 'chegada', e.target.value)} /></td>
                    <td className="p-2 border"><input type="text" placeholder="00:00" className="w-full border-0 p-1" value={formData.horas[idx]?.saida || ''} onChange={e => handleHoraChange(idx, 'saida', e.target.value)} /></td>
                    <td className="p-2 border"><input type="text" placeholder="00:00" className="w-full border-0 p-1" value={formData.horas[idx]?.intervalo || ''} onChange={e => handleHoraChange(idx, 'intervalo', e.target.value)} /></td>
                    <td className="p-2 border"><input type="text" placeholder="00:00" className="w-full border-0 p-1" value={formData.horas[idx]?.deslocamentoIda || ''} onChange={e => handleHoraChange(idx, 'deslocamentoIda', e.target.value)} /></td>
                    <td className="p-2 border"><input type="text" placeholder="00:00" className="w-full border-0 p-1" value={formData.horas[idx]?.deslocamentoVolta || ''} onChange={e => handleHoraChange(idx, 'deslocamentoVolta', e.target.value)} /></td>
                    <td className="p-2 border"><input type="text" placeholder="0" className="w-full border-0 p-1" value={formData.horas[idx]?.distanciaIda || ''} onChange={e => handleHoraChange(idx, 'distanciaIda', e.target.value)} /></td>
                    <td className="p-2 border"><input type="text" placeholder="0" className="w-full border-0 p-1" value={formData.horas[idx]?.distanciaVolta || ''} onChange={e => handleHoraChange(idx, 'distanciaVolta', e.target.value)} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Despesas */}
          <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
            <h2 className="text-md font-semibold text-slate-700 mb-3 uppercase tracking-wide">4. Despesas de Viagem (R$)</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Pedágio</label>
                <input type="number" step="0.01" value={formData.despesas.pedagio} onChange={e => handleDespesaChange('pedagio', e.target.value)} className="w-full border border-slate-300 rounded p-2 text-sm bg-white" placeholder="0.00" />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Refeição</label>
                <input type="number" step="0.01" value={formData.despesas.refeicao} onChange={e => handleDespesaChange('refeicao', e.target.value)} className="w-full border border-slate-300 rounded p-2 text-sm bg-white" placeholder="0.00" />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Hotel</label>
                <input type="number" step="0.01" value={formData.despesas.hotel} onChange={e => handleDespesaChange('hotel', e.target.value)} className="w-full border border-slate-300 rounded p-2 text-sm bg-white" placeholder="0.00" />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Outros</label>
                <input type="number" step="0.01" value={formData.despesas.outros} onChange={e => handleDespesaChange('outros', e.target.value)} className="w-full border border-slate-300 rounded p-2 text-sm bg-white" placeholder="0.00" />
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
