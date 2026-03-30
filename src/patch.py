from signalflow import *


class NotePatch(Patch):
    def __init__(self):
        super().__init__()

        # Basic parameters
        note = self.add_input('note')

        # Oscillator 1 parameters
        osc1_type = self.add_input('osc1_type', 0)
        osc1_offset = self.add_input('osc1_offset', 0)
        osc1_amplitude = self.add_input('osc1_amplitude', 0.0)

        # Oscillator 2 parameters
        osc2_type = self.add_input('osc2_type', 0)
        osc2_offset = self.add_input('osc2_offset', 0)
        osc2_amplitude = self.add_input('osc2_amplitude', 0.0)

        # Oscillator 3 parameters
        osc3_type = self.add_input('osc3_type', 0)
        osc3_offset = self.add_input('osc3_offset', 0)
        osc3_amplitude = self.add_input('osc3_amplitude', 0.0)

        # Calculate frequencies
        b_freq = MidiNoteToFrequency(note)
        u_freq = MidiNoteToFrequency(note + 1)
        l_freq = MidiNoteToFrequency(note - 1)

        # Generate output for Oscillator 1
        osc1_freq = If(
            GreaterThan(osc1_offset, Constant(0.0)),
            b_freq + (u_freq - b_freq) * osc1_offset,
            b_freq + (b_freq - l_freq) * osc1_offset
        )
        osc1_type = If(
            Equal(osc1_type, Constant(0)),
            SineOscillator(osc1_freq),
            If(
                Equal(osc1_type, Constant(1)),
                SawOscillator(osc1_freq),
                If(
                    Equal(osc1_type, Constant(2)),
                    SquareOscillator(osc1_freq),
                    TriangleOscillator(osc1_freq)
                )
            )
        )
        osc1_output = osc1_type * osc1_amplitude

        # Generate output for Oscillator 2
        osc2_freq = If(
            GreaterThan(osc2_offset, Constant(0.0)),
            b_freq + (u_freq - b_freq) * osc2_offset,
            b_freq + (b_freq - l_freq) * osc2_offset
        )
        osc2_type = If(
            Equal(osc2_type, Constant(0)),
            SineOscillator(osc2_freq),
            If(
                Equal(osc2_type, Constant(1)),
                SawOscillator(osc2_freq),
                If(
                    Equal(osc2_type, Constant(2)),
                    SquareOscillator(osc2_freq),
                    TriangleOscillator(osc2_freq)
                )
            )
        )
        osc2_output = osc2_type * osc2_amplitude

        # Generate output for Oscillator 2
        osc3_freq = If(
            GreaterThan(osc3_offset, Constant(0.0)),
            b_freq + (u_freq - b_freq) * osc3_offset,
            b_freq + (b_freq - l_freq) * osc3_offset
        )
        osc3_type = If(
            Equal(osc3_type, Constant(0)),
            SineOscillator(osc3_freq),
            If(
                Equal(osc3_type, Constant(1)),
                SawOscillator(osc3_freq),
                If(
                    Equal(osc3_type, Constant(2)),
                    SquareOscillator(osc3_freq),
                    TriangleOscillator(osc3_freq)
                )
            )
        )
        osc3_output = osc3_type * osc3_amplitude

        # Mix output
        output = StereoPanner(osc1_output + osc2_output + osc3_output)

        # Send output
        self.set_output(output)
        self.set_auto_free(True)
