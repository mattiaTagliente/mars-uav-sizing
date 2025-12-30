# Example usage

atm = MarsAtmosphere()
state = atm.at_altitude(-3000)  # -3 km elevation

print(f"Density: {state.rho:.4f} kg/m³")
print(f"Temperature: {state.T:.1f} K")
```
