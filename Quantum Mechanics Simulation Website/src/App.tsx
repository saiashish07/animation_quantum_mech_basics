import { useState } from "react";
import { motion } from "motion/react";
import { InfiniteWell } from "./components/InfiniteWell";
import { FiniteBarrier } from "./components/FiniteBarrier";
import { QuantumHarmonicOscillator } from "./components/QuantumHarmonicOscillator";
import { QuantumTunneling } from "./components/QuantumTunneling";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "./components/ui/tabs";
import { Card } from "./components/ui/card";
import { Box, Zap, Waves, Activity } from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState("infinite");

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900 text-slate-100">
      {/* Header */}
      <header className="border-b border-blue-500/20 bg-slate-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-6">
          <div className="text-center">
            <motion.h1
              className="text-blue-100 mb-2"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              Quantum Mechanics Visualizer
            </motion.h1>
            <motion.p
              className="text-blue-400/70"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              Interactive simulations to understand quantum
              phenomena
            </motion.p>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="container mx-auto px-6 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Tabs
            value={activeTab}
            onValueChange={setActiveTab}
            className="w-full"
          >
            <TabsList className="grid w-full grid-cols-4 bg-slate-900/50 border border-blue-500/20 mb-8 h-auto">
              <TabsTrigger
                value="infinite"
                className="data-[state=active]:bg-blue-600/40 data-[state=active]:text-blue-100 flex flex-col gap-1 py-3"
              >
                <Box className="w-5 h-5" />
                <span className="text-xs">
                  Infinite Potential Well
                </span>
              </TabsTrigger>
              <TabsTrigger
                value="finite"
                className="data-[state=active]:bg-blue-600/40 data-[state=active]:text-blue-100 flex flex-col gap-1 py-3"
              >
                <Activity className="w-5 h-5" />
                <span className="text-xs">
                  Finite Potential Barrier
                </span>
              </TabsTrigger>
              <TabsTrigger
                value="harmonic"
                className="data-[state=active]:bg-blue-600/40 data-[state=active]:text-blue-100 flex flex-col gap-1 py-3"
              >
                <Waves className="w-5 h-5" />
                <span className="text-xs">
                  Harmonic Oscillator
                </span>
              </TabsTrigger>
              <TabsTrigger
                value="tunneling"
                className="data-[state=active]:bg-blue-600/40 data-[state=active]:text-blue-100 flex flex-col gap-1 py-3"
              >
                <Zap className="w-5 h-5" />
                <span className="text-xs">
                  Quantum Tunneling
                </span>
              </TabsTrigger>
            </TabsList>

            <TabsContent value="infinite" className="mt-0">
              <Card className="bg-slate-900/30 border-blue-500/20 backdrop-blur-sm p-6">
                <InfiniteWell />
              </Card>
            </TabsContent>

            <TabsContent value="finite" className="mt-0">
              <Card className="bg-slate-900/30 border-blue-500/20 backdrop-blur-sm p-6">
                <FiniteBarrier />
              </Card>
            </TabsContent>

            <TabsContent value="harmonic" className="mt-0">
              <Card className="bg-slate-900/30 border-blue-500/20 backdrop-blur-sm p-6">
                <QuantumHarmonicOscillator />
              </Card>
            </TabsContent>

            <TabsContent value="tunneling" className="mt-0">
              <Card className="bg-slate-900/30 border-blue-500/20 backdrop-blur-sm p-6">
                <QuantumTunneling />
              </Card>
            </TabsContent>
          </Tabs>
        </motion.div>

        {/* Educational note */}
        <motion.div
          className="mt-8 p-4 bg-blue-950/30 border border-blue-500/20 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <p className="text-blue-300/70 text-sm text-center">
            💡 Use the controls to adjust parameters and observe
            how quantum states change. Each visualization shows
            the wave function ψ(x), probability density |ψ|²,
            and energy levels.
          </p>
        </motion.div>
      </main>
    </div>
  );
}