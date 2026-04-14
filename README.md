# SDN Firewall using Mininet and POX

## Student Details
- Name: Sharvari Naik
- SRN: PES1UG24CS431
- Course:Computer Networks Lab

---

##Problem Statement
The objective of this project is to implement a Software Defined Networking (SDN) solution using Mininet and POX controller to demonstrate controller-switch interaction, flow rule design, and traffic control.

A firewall mechanism is implemented to selectively block communication between specific hosts.

---

## Concept
In SDN, the control plane is separated from the data plane. The controller decides how packets should be handled by installing flow rules in switches.

This project modifies a learning switch to include firewall logic using match-action rules.

---

## Topology
Linear topology with:
- 2 switches (s1, s2)
- 4 hosts (h1s1, h1s2, h2s1, h2s2)

