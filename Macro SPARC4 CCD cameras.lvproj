﻿<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="18008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="main.vi" Type="VI" URL="../main.vi"/>
		<Item Name="TESTE.vi" Type="VI" URL="../CCD/TESTE.vi"/>
		<Item Name="Interface.lvclass" Type="LVClass" URL="../Interface/Interface.lvclass"/>
		<Item Name="State Machine.lvclass" Type="LVClass" URL="../State Machine/State Machine.lvclass"/>
		<Item Name="CCD.lvclass" Type="LVClass" URL="../CCD/CCD.lvclass"/>
		<Item Name="Cooler.lvclass" Type="LVClass" URL="../Cooler/Cooler.lvclass"/>
		<Item Name="Timer.lvclass" Type="LVClass" URL="../Timer/Timer.lvclass"/>
		<Item Name="JSON.lvclass" Type="LVClass" URL="../JSON/JSON.lvclass"/>
		<Item Name="SetEMCCDGain.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetEMCCDGain.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="user.lib" Type="Folder">
				<Item Name="Error Code Offset global.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d_internal.llb/Error Code Offset global.vi"/>
				<Item Name="Add ECO For LabVIEW.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d_internal.llb/Add ECO For LabVIEW.vi"/>
				<Item Name="Subtract ECO For DLL.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d_internal.llb/Subtract ECO For DLL.vi"/>
				<Item Name="Join Strings.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d_internal.llb/Join Strings.vi"/>
				<Item Name="Get Error Source.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d_internal.llb/Get Error Source.vi"/>
				<Item Name="Add ECO For DLL.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d_internal.llb/Add ECO For DLL.vi"/>
				<Item Name="Error Code Enum typedef.ctl" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/Error Code Enum typedef.ctl"/>
				<Item Name="Error Code Handler.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d_internal.llb/Error Code Handler.vi"/>
				<Item Name="U32 To Error Code Enum.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d_internal.llb/U32 To Error Code Enum.vi"/>
				<Item Name="GetStatus.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/GetStatus.vi"/>
				<Item Name="AbortAcquisition.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/AbortAcquisition.vi"/>
				<Item Name="AcquisitionMode_mode typedef.ctl" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/AcquisitionMode_mode typedef.ctl"/>
				<Item Name="TriggerMode_mode typedef.ctl" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/TriggerMode_mode typedef.ctl"/>
				<Item Name="HSSpeed_type typedef.ctl" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/HSSpeed_type typedef.ctl"/>
				<Item Name="Shutter_type typedef.ctl" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/Shutter_type typedef.ctl"/>
				<Item Name="Shutter_mode typedef.ctl" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/Shutter_mode typedef.ctl"/>
				<Item Name="ReadMode_mode typedef.ctl" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/ReadMode_mode typedef.ctl"/>
				<Item Name="StartAcquisition.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/StartAcquisition.vi"/>
				<Item Name="GetAcquiredData16.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/GetAcquiredData16.vi"/>
				<Item Name="Initialize.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/Initialize.vi"/>
				<Item Name="GetDetector.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/GetDetector.vi"/>
				<Item Name="GetCameraSerialNumber.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/GetCameraSerialNumber.vi"/>
				<Item Name="SetAcquisitionMode.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetAcquisitionMode.vi"/>
				<Item Name="SetReadMode.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetReadMode.vi"/>
				<Item Name="SetVSSpeed.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetVSSpeed.vi"/>
				<Item Name="SetTriggerMode.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetTriggerMode.vi"/>
				<Item Name="SetImage.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetImage.vi"/>
				<Item Name="SetExposureTime.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetExposureTime.vi"/>
				<Item Name="SetShutter.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetShutter.vi"/>
				<Item Name="SetADChannel.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetADChannel.vi"/>
				<Item Name="SetHSSpeed.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetHSSpeed.vi"/>
				<Item Name="SetPreAmpGain.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetPreAmpGain.vi"/>
				<Item Name="SetFrameTransferMode.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetFrameTransferMode.vi"/>
				<Item Name="SetVSAmplitude.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetVSAmplitude.vi"/>
				<Item Name="SetNumberKinetics.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetNumberKinetics.vi"/>
				<Item Name="SetTemperature.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SetTemperature.vi"/>
				<Item Name="ShutDown.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/ShutDown.vi"/>
				<Item Name="CoolerOFF.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/CoolerOFF.vi"/>
				<Item Name="CoolerON.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/CoolerON.vi"/>
				<Item Name="GetTemperature.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/GetTemperature.vi"/>
				<Item Name="IsCoolerOn.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/IsCoolerOn.vi"/>
				<Item Name="GetTemperatureRange.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/GetTemperatureRange.vi"/>
				<Item Name="GetImages16.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/GetImages16.vi"/>
				<Item Name="SYSTEMTIME structure typedef.ctl" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/SYSTEMTIME structure typedef.ctl"/>
				<Item Name="U16 Array To SYSTEMTIME.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d_internal.llb/U16 Array To SYSTEMTIME.vi"/>
				<Item Name="GetMetaDataInfo.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/GetMetaDataInfo.vi"/>
				<Item Name="GetRelativeImageTimes.vi" Type="VI" URL="/&lt;userlib&gt;/atmcd32d.llb/GetRelativeImageTimes.vi"/>
				<Item Name="gfitsio.lvlib" Type="Library" URL="/&lt;userlib&gt;/gfitsio/gfitsio.lvlib"/>
			</Item>
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="compatFileDialog.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/compatFileDialog.vi"/>
				<Item Name="GetHelpDir.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetHelpDir.vi"/>
				<Item Name="BuildHelpPath.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/BuildHelpPath.vi"/>
				<Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
				<Item Name="Get String Text Bounds.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Get String Text Bounds.vi"/>
				<Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
				<Item Name="Convert property node font to graphics font.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Convert property node font to graphics font.vi"/>
				<Item Name="Longest Line Length in Pixels.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Longest Line Length in Pixels.vi"/>
				<Item Name="LVRectTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVRectTypeDef.ctl"/>
				<Item Name="Three Button Dialog CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog CORE.vi"/>
				<Item Name="Three Button Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog.vi"/>
				<Item Name="DialogTypeEnum.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogTypeEnum.ctl"/>
				<Item Name="Not Found Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Not Found Dialog.vi"/>
				<Item Name="Set Bold Text.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set Bold Text.vi"/>
				<Item Name="eventvkey.ctl" Type="VI" URL="/&lt;vilib&gt;/event_ctls.llb/eventvkey.ctl"/>
				<Item Name="TagReturnType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/TagReturnType.ctl"/>
				<Item Name="ErrWarn.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/ErrWarn.ctl"/>
				<Item Name="Details Display Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Details Display Dialog.vi"/>
				<Item Name="Search and Replace Pattern.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Search and Replace Pattern.vi"/>
				<Item Name="Find Tag.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find Tag.vi"/>
				<Item Name="Format Message String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Format Message String.vi"/>
				<Item Name="Error Code Database.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Code Database.vi"/>
				<Item Name="GetRTHostConnectedProp.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetRTHostConnectedProp.vi"/>
				<Item Name="Set String Value.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set String Value.vi"/>
				<Item Name="Check Special Tags.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Check Special Tags.vi"/>
				<Item Name="General Error Handler Core CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler Core CORE.vi"/>
				<Item Name="DialogType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogType.ctl"/>
				<Item Name="General Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler.vi"/>
				<Item Name="Merge Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Merge Errors.vi"/>
				<Item Name="ex_CorrectErrorChain.vi" Type="VI" URL="/&lt;vilib&gt;/express/express shared/ex_CorrectErrorChain.vi"/>
				<Item Name="subFile Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/express/express input/FileDialogBlock.llb/subFile Dialog.vi"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="Application Directory.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Application Directory.vi"/>
			</Item>
			<Item Name="atmcd32d.dll" Type="Document" URL="../../../../../Program Files (x86)/National Instruments/LabVIEW 2018/atmcd32d.dll"/>
			<Item Name="User32.dll" Type="Document" URL="User32.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="gfitsio-refnum.ctl" Type="VI" URL="../../../../../Documents and Settings/ggatling/My Documents/p4depot/LabVIEW 8.5/applications/LP_ONESHOT/user.lib/gfitsio/gfitsio-refnum.ctl"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
