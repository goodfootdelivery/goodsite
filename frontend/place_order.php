<?php



/*

Template Name: Place an Order

*/


class Wp_Layout_Template extends Wp_Layout {

	private $oUser;
	private $aAddrDelivery;
	private $aAddrPickup;
	//
	public function init( $bUnshift = FALSE ) {
		parent::init( $bUnshift );
		$this->oUser = $this->newMember();
		if ( $this->oUser->getId() ) {
			$aAddresses = $this->newMember_Address_Query( array(
				'object_id' => $this->oUser->getId(),
				'showposts' => -1
			), FALSE );

			$aAddrTypes = Geko_Wp_Enumeration_Query::getSet( 'user-address-type' );
			$this->aAddrDelivery = $aAddresses->subsetAddressTypeId( $aAddrTypes->getValueFromSlug( 'delivery' ) );
			$this->aAddrPickup = $aAddresses->subsetAddressTypeId( $aAddrTypes->getValueFromSlug( 'pick-up' ) );
		}
		return $this;
	}
	//
	public function echoEnqueue() {
		wp_enqueue_script( 'geko-jquery-json' );
		wp_enqueue_script( 'geko-jquery-form' );
		wp_enqueue_script( 'geko-jquery-ui-datepicker' );
		wp_enqueue_style( 'geko-jquery-ui-wp' );
	}
	//
	public function echoHeadLate() {
		$aJsonParams = array(
			'script' => array(
				'url' => get_bloginfo( 'url' ),
				'process' => get_bloginfo( 'template_directory' ) . '/services/process.php',
				'wp_login' => get_bloginfo( 'url' ) . '/wp-login.php'
			),
			'status' => array(
				'login_success' => Geko_Wp_Login::STAT_LOGIN_SUCCESS,
				'order_processed' => Wp_Service_ProcessOrder::STAT_ORDER_PROCESSED,
				'new_user' => Wp_Service_ProcessOrder::STAT_NEW_USER,
				'user_exists' => Wp_Service_ProcessOrder::STAT_USER_EXISTS,
				'register' => Wp_Service_ProcessOrder::STAT_REGISTER
			),
			'year' => date( 'Y' ),
			'is_logged_in' => ( ( $this->oUser->getId() ) ? TRUE : FALSE ),
			'show_login_form' => ( ( $_GET[ 'login' ] ) ? TRUE : FALSE ),
			'has_addr_delivery' => ( ( ( $this->aAddrDelivery ) && ( $this->aAddrDelivery->count() > 0 ) ) ? TRUE : FALSE ),
			'has_addr_pickup' => ( ( ( $this->aAddrPickup ) && ( $this->aAddrPickup->count() > 0 ) ) ? TRUE : FALSE )
		);
		
		?>


		
		

<link rel="stylesheet" type="text/css" href="<?php bloginfo( 'template_directory' ); ?>/styles/temp_style.css" media="screen" />
<link rel="stylesheet" type="text/css" href="<?php bloginfo( 'template_directory' ); ?>/styles/order_form.css?v=123456" media="screen" />

		
		<!-- GEOCOMPLETE -->	
		<script src="http://maps.googleapis.com/maps/api/js?sensor=false&amp;libraries=places"></script>	
		<script type="text/javascript" src="http://goodfootdelivery.com/js/jquery.geocomplete.js"></script>

		<script type="text/javascript">		
			jQuery(document).ready(function($) { 
				$( ".pickup" ).geocomplete({
					details: "#start",
					detailsAttribute: "geo",
					types: ["geocode"],
				});
				$( ".dropoff" ).geocomplete({
					details: "#end",
					detailsAttribute: "geo",
					types: ["geocode"],
				});
				$( '#orderSubmit' ).click(function() {
					var errors = '';
					var borderDefinition = 'solid 2px #f00';
					var oParams = <?php echo Zend_Json::encode( $aJsonParams ); ?>;

					var addressFrom = $.trim( $( '#pick-up-address' ).val() );
					var unitFrom = $.trim( $( '#pick-up-unit' ).val() );
					var nameFrom = $.trim( $( '#pick-up-name' ).val() );
					var phoneFrom = $.trim( $( '#pick-up-phone' ).val() );

					var addressTo = $.trim( $( '#drop-off-address' ).val() );
					var unitTo = $.trim( $( '#drop-off-unit' ).val() );
					var nameTo = $.trim( $( '#drop-off-name' ).val() );
					var phoneTo = $.trim( $( '#drop-off-phone' ).val() );

					var date = $.trim( $( '#date' ).val() );
					var readyTimeHours = $.trim( $( '#readyTimeHours' ).val() );
					var readyTimeMinutes = $.trim( $( '#readyTimeMinutes' ).val() );

					var qtdEnvelopes = $.trim( $( '#qtdEnvelopes' ).val() );
					var qtdBoxorBag = $.trim( $( '#qtdBoxorBag' ).val() );
					var qtdOther = $.trim( $( '#qtdOther' ).val() );

					$( '#placeOrder input, #placeOrder select, #placeOrder textarea' ).css( 'border', 'none' );

					if ( $( '#useFromManual' ).attr( 'checked' ) ) {
						if ( !addressFrom ) {
							errors += 'Please enter the pickup address - you must pick an address fromt the google selector.<br />';
							$( '#pick-up-field' ).css( 'border', borderDefinition);
						};
						if ( !nameFrom ) {
							errors += 'Please enter the pickup name/company.<br />';
							$( '#pick-up-name' ).css( 'border', borderDefinition);
						};
						if( !phoneFrom ) {
							phoneFrom = 'N/A'
						}
					}
					

					if ( $( '#useToManual' ).attr( 'checked' ) ) {
						if ( !addressTo ) {
							errors += 'Please enter the destination address - you must pick an address fromt the google selector.<br />';
							$( '#drop-off-field' ).css( 'border', borderDefinition);
						};
						if ( !nameTo ) {
							errors += 'Please enter the destination name/company.<br />';
							$( '#drop-off-name' ).css( 'border', borderDefinition);
						};
						if( !phoneTo ) {
							phoneTo = 'N/A'
						}
					}


					if ( !date || (date == "DD/MM/YYYY") ) {
						errors += 'Please enter a valid date<br />';
						$( '#date' ).css( 'border', borderDefinition);
					}

					//if (!readyTimeHours || isNaN(readyTimeHours) || 
					//	readyTimeHours > 12 || !readyTimeMinutes ||
					//   	isNaN(readyTimeMinutes) || readyTimeMinutes > 59 ) {

					//	errors += 'Please enter a valid time<br />';
					//	$( '#readyTimeHours' ).css( 'border', borderDefinition);
					//	$( '#readyTimeMinutes' ).css( 'border', borderDefinition);
					//}

					if (!qtdEnvelopes && !qtdBoxorBag && !qtdOther) {
						errors += 'Please specify your order<br />';	
						$( '#qtdEnvelopes' ).css( 'border', borderDefinition );
						$( '#qtdBoxorBag' ).css( 'border', borderDefinition );
						$( '#qtdOther' ).css( 'border', borderDefinition );
					}

					if ( !oParams.is_logged_in ) {

						// only show if not logged in

						if ( !contactName ) {
							errors += 'Please enter your name<br />';
							$( '#contactName' ).css( 'border', borderDefinition );
						}

						if ( !contactEmail ) {
							errors += 'Please enter your email<br />';
							$( '#contactEmail' ).css( 'border', borderDefinition );
						} else {
							var emailTest = /^[a-z0-9\._-]+@([a-z0-9_-]+\.)+[a-z]{2,6}$/i;

							if ( !emailTest.test( contactEmail ) ) {
								errors += 'Please enter a valid email address<br />';
								$( '#contactEmail' ).css( 'border', borderDefinition );
							}
						}
					}

					if ( errors ) {
						$( '#formErrors' ).html( errors ).show( 300 );
					} else {
						$( '#formErrors' ).hide();
						$( this ).parent().find( '.ajax_loading' ).show();

						if ( oParams.is_logged_in ) {
							// already logged in, so process order
							// fProcessOrder( '#order_section' );
							$('form#placeOrder').submit()

						} else {
							// login or register

							$.post(
								oParams.script.process,
								{
									action: 'Wp_Service_ProcessOrder',
									subaction: 'check_email',
									email: $( '#contactEmail' ).val(),
									name: $( '#contactName' ).val()
								},

								function ( res ) {
									$( '#order_section' ).hide( 300 );
									if ( oParams.status.new_user == parseInt( res.status ) ) {
										$( '#rsEmail' ).val( $( '#contactEmail' ).val() );
										$( '#rsFirstName' ).val( res.firstname );
										$( '#rsLastName' ).val( res.lastname );
										$( '#register_section' ).show( 300 );
									} else if ( oParams.status.user_exists == parseInt( res.status ) ) {

										// setup login form so that it places and order
										$( '#botLogin span' ).html( 'Login and Place Order' );
										$( '#lsEmail' ).attr( 'disabled', 'disabled' );
										$( '#lsEmail' ).val( $( '#contactEmail' ).val() );
										$( '#login_section' ).show( 300 );

									} else {
										$( '#formErrors' ).html( 'There was an error processing the order. Please try again.' );
									}
									$( '.ajax_loading' ).hide();
								},
								'json'
							);
						}
					}

					return false;

				});
			});
		</script>		

    	<script type="text/javascript">
			jQuery( document ).ready( function( $ ) {
				var borderDefinition = 'solid 2px #f00';
				var oParams = <?php echo Zend_Json::encode( $aJsonParams ); ?>;
				//

				

				var fSetUserStatus = function( data ) {
					// dynamically set the user status section
					$( '#container div.user_status' ).html(
						'<ul>' + 
							'<li><strong>Logged in as:<\/strong> ' + data.full_name + '<\/li>' + 
							'<li class="loginButton"><a href="' + oParams.script.url + '/address-book/">Address Book<\/a><\/li>' + 
							'<li class="loginButton"><a href="' + oParams.script.url + '/order-history/">Order History<\/a><\/li>' + 
							'<li class="loginButton"><a href="' + oParams.script.url + '/account-info/">Account Info<\/a><\/li>' + 
							'<li class="loginButton"><a href="' + data.logout_url + '" test="' + data.test + '">Log-out<\/a><\/li>' + 
						'<\/ul>'
					);
				}

				$( '#date' ).datepicker( {
					changeMonth: true,
					changeYear: false,
					yearRange: '1900:' + oParams.year,
					minDate: new Date(),
					beforeShowDay: $.datepicker.noWeekends

				} );

				$( '#useFromManual' ).click( function() {
					$( '#manualSectionFrom' ).show( 300 );
					$( '#addrBookSectionFrom' ).hide( 300 );
				} );

				$( '#useFromAddrBook' ).click( function() {
					$( '#manualSectionFrom' ).hide( 300 );
					$( '#addrBookSectionFrom' ).show( 300 );
				} );

				$( '#useToManual' ).click( function() {
					$( '#manualSectionTo' ).show( 300 );
					$( '#addrBookSectionTo' ).hide( 300 );				
				} );

				

				$( '#useToAddrBook' ).click( function() {
					$( '#manualSectionTo' ).hide( 300 );
					$( '#addrBookSectionTo' ).show( 300 );				
				} );
				
				//// init

				$( '#orderConfirmation, #formErrors, #register_section, #login_section, .ajax_loading, #addrBookSectionTo, #addrBookSectionFrom, #print_waybill' ).hide();


				if ( !oParams.has_addr_pickup ) $( '#toggleFrom' ).hide();
				if ( !oParams.has_addr_delivery ) $( '#toggleTo' ).hide();
				if ( oParams.show_login_form ) $( '#botLoginMain' ).click();
			} );
		</script>
    	<?php	
	}
	//
		public function echoContent() {
		//$aServiceLevels = Geko_Wp_Enumeration_Query::getSet( 'user-order-service-level' );
		//$oLocation = Wp_Member_Location_Manage::getInstance()->init();
		?>
			<?			if ( is_user_logged_in() ) { ?>
        <div id="submitOrder">
        	<div id="formErrors"></div>
    		<form id='placeOrder' action="/place-an-order-beta" method="post">
			


			
			<!-- <input name="pu_street_number"  id="pu_street_number" type="hidden"></input>
			<input  name="pu_street_name" id="pu_route" type="hidden"></input>
			<input name="pu_city"  id="pu_locality" type="hidden"></input>
			<input  name="pu_province" id="pu_administrative_area_level_1" type="hidden"></input>
			<input  name="pu_postal_code"  id="pu_postal_code" type="hidden"></input>
			<input  name="pu_country" id="pu_country" type="hidden"></input>
	
			<input  name="pu_suite"  id="pu_suite" type="hidden"></input>
			<input  name="pu_contact"  id="pu_contact" type="hidden"></input>
			<input name="pu_company_name"  id="pu_company_name" type="hidden"></input>
			<input  name="pu_contact_phone"  id="pu_contact_phone" type="hidden"></input>
			<input  type="hidden" name="pu_lat"  id="pu_lat" ></input>
			<input  type="hidden" name="pu_lng"  id="pu_lng" ></input>
			
			
			<input type="hidden"name="do_street_number"  id="do_street_number" ></input>
			<input type="hidden" name="do_street_name" id="do_route"></input>
			<input type="hidden" name="do_city"  id="do_locality" ></input>
			<input type="hidden" name="do_province" id="do_administrative_area_level_1" ></input>
			<input type="hidden" name="do_postal_code"  id="do_postal_code" ></input>
			<input type="hidden" name="do_country" id="do_country" t></input>
			<input type="hidden" name="do_suite"  id="do_suite" ></input>
			 <input type="hidden" name="do_contact"  id="do_contact" ></input>
			 <input type="hidden" name="do_company_name"  id="do_company_name" ></input>
			 <input type="hidden" name="do_contact_phone"  id="do_contact_phone" ></input>
			<input  type="hidden" name="do_lat"  id="do_lat" ></input>
			<input  type="hidden" name="do_lng"  id="do_lng" ></input>  -->
				

			<div id="order_section">
				<table id="tableOrder" width="687">
						<tr>
							<td width="332" valign="top">
							<p></p>
								<h2>Pick Up From</h2>
									<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_half.gif" />
								<p></p>
								<table id="toggleFrom" class="formLine" width="100%">
									<tr>
										<td width="120px"><label>Manual Entry</label></td>
										<td class="radioCheck" width="24px"><input id="useFromManual" name="useFrom" type="radio" value="manual" checked="checked" /></td>
										<td width="15px">&nbsp;</td>
										<td width="125px"><label>Address Book</label></td>
										<td class="radioCheck" width="24px"><input id="useFromAddrBook" name="useFrom" type="radio" value="addr_book" /></td>
									</tr>
								</table>
								<div id="manualSectionFrom">
									<table class="formLine" width="100%">
										<tr>
											<td style="padding-right:10px" width="85%">
											   <div id="locationField">
      												<div id="start">
														<label for="pickup-formatted">Address <font color="red">*</font></label>
														<input id="pick-up-field" name="pickup-formatted" class="pickup" type="text" placeholder="ie 1 Toronto St." >
														<!-- <hidden></hidden> -->
														<input geo="formatted_address" 
															name="pick-up-address" 
															id="pick-up-address" type="hidden">
														<input geo="location" name="pick-up-coords" type="hidden" />
													</div>
										
												</div>
											</td>
											<td width="15%">
												<label>Unit</label>
												<input name="pick-up-unit" type="text" placeholder="ie #303">
											
											</td>
										</tr>
									</table>
									
								<table class="formLine" width="100%">
										<tr>	
											<!-- <td><label>Name</label></td> -->
											<td style="padding-right:10px" width="65%">
												<label for="pick-up-name">Care Of <font color="red">*</font></label>
												<input id="pick-up-name" name="pick-up-care-of" type="text" placeholder="name, company">
											
											</td>
											
											<!-- <td nowrap>&nbsp;<label>Phone</label></td> -->
											<td width="35%">
												<label for="pick-up-phone">Phone</label>
												<input name="pick-up-phone" type="text" placeholder="416-555-1234">
											</td>
											
										</tr>
								</table>
								<!-- <table class="formLine" width="100%">
										<tr>	
										<td><label>Company</label></td>
											<td width="50%">
											<input name="pick-up-company" type="text" placeholder="eg: Dunder-Mifflin Paper Company">
										</td>
										
										<td nowrap>&nbsp;<label>Unit</label></td>
											<td width="50%">
											<input name="pick-up-unit" type="text" placeholder="eg #303">
											
											</td>
										
										</tr>
								</table> -->
								
								</div>

								
								<div id="addrBookSectionFrom">

									<table class="formLine" width="100%">

										<tr>

											<td><label>Company</label></td>

											<td width="100%"><?php

											

											if (

												( $this->aAddrPickup ) && 

												( $this->aAddrPickup->count() > 0 )

											) {

												?>

												<select id="addrBookIdFrom" name="addrBookIdFrom">

													<?php echo $this->aAddrPickup->implode( array( '<option value="##Id##">##Title##</option>', '' ) ); ?>

												</select>

												<?php

											}

											

											?></td>

										</tr>

									</table>

								</div>

								

							</td>

							<td width="23">&nbsp;</td>

							<td width="332" valign="top">

								
<p></p>


								<h2>Deliver To</h2>

								<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_half.gif" />
								<p></p>

								<table id="toggleTo" class="formLine" width="100%">
									<tr>
										<td width="120px"><label>Manual Entry</label></td>
										<td width="24px"class="radioCheck">
											<input id="useToManual" name="useTo" type="radio" value="manual" checked="checked" /></td>
										<td width="15px">&nbsp;</td>
										<td width="125px"><label>Address Book</label></td>
										<td width="24px" class="radioCheck"><input id="useToAddrBook" name="useTo" type="radio" value="addr_book" /></td>
									</tr>
								</table>

								<div id="manualSectionTo">
									<table class="formLine" width="100%">
										<tr>
											<td style="padding-right:10px" width="85%">
											   <div id="locationField">
      												<div id="end">
														<label for="drop-off-formatted">Address <font color="red">*</font></label>
														<input id="drop-off-field" name="drop-off-formatted" class="dropoff" type="text" placeholder="ie: 720 Bathurst St." >
														<!-- <hidden></hidden> -->
														<input geo="formatted_address" 
															name="drop-off-address" 
															id="drop-off-address" type="hidden">
														<input geo="location" name="drop-off-coords" type="hidden" />
													</div>
										
												</div>
											</td>
											<td width="15%">
												<label>Unit</label>
												<input name="drop-off-unit" type="text" placeholder="ie 3300">
											
											</td>
										</tr>
									</table>
									<!-- <table class="formLine" width="100%">
										<tr>
											<td width="100%">
												<div id="locationField">
													<div id="end">
														<input class="dropoff" type="text">
														<input geo="formatted_address" 
															name="drop-off-address" 
															id="drop-off-address" placeholder="Street (i.e. 720 Bathurst St)" type="hidden">
															</input>
														<input geo="location" name="drop-off-coords" type="hidden">
													</div>
												</div>
											</td>
										</tr>
									</table> -->
								<table class="formLine" width="100%">
										<tr>	
											<!-- <td><label>Name</label></td> -->
											<td style="padding-right:10px" width="65%">
												<label for="drop-off-name">Care Of <font color="red">*</font></label>
												<input id="drop-off-name" name="drop-off-care-of" type="text" placeholder="name, company">
											
											</td>
											
											<!-- <td nowrap>&nbsp;<label>Phone</label></td> -->
											<td width="35%">
												<label for="drop-off-phone">Phone</label>
												<input name="drop-off-phone" type="text" placeholder="416-555-1234">
											</td>
											
										</tr>
								</table>

								<!-- <table class="formLine" width="100%">
										<tr>	<td><label>Name</label></td>
											<td width="50%">
											<input name="drop-off-unit" type="text" placeholder="eg: Art">
											
											</td>
											
											<td nowrap>&nbsp;<label>Phone</label></td>
											<td width="50%">
											<input name="drop-off-phone" type="text" placeholder="416-555-1234">
											
											</td>
											
										</tr>
								</table> -->
								<!-- <table class="formLine" width="100%">
										<tr>	
										<td><label>Company</label></td>
											<td width="50%">
											<input name="drop-off-company" type="text" placeholder="eg: Vandolay Industries">
										</td>
										
										<td nowrap>&nbsp;<label>Unit</label></td>
											<td width="50%">
											<input name="drop-off-unit" type="text" placeholder="eg #303">
											
											</td>
										
										</tr>
								</table> -->
								

								</div>

								<div id="addrBookSectionTo">

									<table class="formLine" width="100%">

										<tr>

											<td><label>Company</label></td>

											<td width="100%"><?php

											

											if (

												( $this->aAddrDelivery ) && 

												( $this->aAddrDelivery->count() > 0 )

											) {

												?>

												<select id="addrBookIdTo" name="addrBookIdTo">

													<?php echo $this->aAddrDelivery->implode( array( '<option value="##Id##">##Title##</option>', '' ) ); ?>

												</select>

												<?php

											}

											

											?></td>

										</tr>

									</table>

								</div>

								

							</td>

						</tr>

					</table>

					<table id="tableOrder" width="687">

							<tr>

							<td width="332" valign="top">

							
								<p></p>
								<h2>Pick Up Time <font color="red">*</font></h2>
								<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_half.gif" />
								<p></p>

							<table cellspacing="5" align="center">
										<tr>
											<td><label>Date:</label></td>
											<td><input id="date" name="ready-date" type="text" style="width:85px;" value="<?
											if (!date('N', strtotime($next_date) >= 6)){
											echo date("m/d/Y");
											}
											?>" /></td>
									
											<td nowrap><label>Time:</label></td>
											<td nowrap>
											<select name="time-select">
											<option value = "9:00 AM">9:00 AM</option>
											<option value = "9:30 AM">9:30 AM</option>
											<option value = "10:00 AM">10:00 AM</option>
											<option value = "10:30 AM">10:30 AM</option>
											<option value = "11:00 AM">11:00 AM</option>
											<option value = "11:30 AM">11:30 AM</option>
											<option value = "12:00 PM">12:00 PM</option>
											<option value = "12:30 PM">12:30 PM</option>
											<option value = "1:00 PM">1:00 PM</option>
											<option value = "1:30 PM">1:30 PM</option>
											<option value = "2:00 PM">2:00 PM</option>
											<option value = "2:30 PM">2:30 PM</option>
											<option value = "3:00 PM">3:00 PM</option>
											<option value = "3:30 PM">3:30 PM</option>
											<option value = "4:00 PM">4:00 PM</option>
											</select>
											</td>
											<!-- <td nowrap>
												<input id="readyTimeHours" name="readyTimeHours" type="text" style="width:18px;" value="<? echo date("h"); ?>" />
												<b>:</b>
												<input id="readyTimeMinutes" name="readyTimeMinutes" type="text" style="width:18px;" value="<? echo date("i"); ?>"/>
												<select id="timeSelect" name="timeSelect" style="width:54px; margin-left:5px;">
											
													
											
												<? $AMPM = date("a");
												if ($AMPM == 'am'){
													?>
													<option value="AM">AM</option>
													<option value="PM">PM</option>
													<?
												}
												if ($AMPM == 'pm'){
												?>
													<option value="PM">PM</option>
													<option value="AM">AM</option>
													<?
												}
												?>
													</select>
											</td> -->
										</tr>
								</table>

														</td>

							<td width="23">&nbsp;</td>

							<td width="332" valign="top">

								
								<p></p>
								<h2>Package Details <font color="red">*</font></h2>
								<img src="<?php bloginfo( 'template_directory' ); ?>/images/img_bottom_border_half.gif" />
								<p></p>
								
								<table cellspacing="5">
												<tr>
													<td align="right"><label>Envelope: </label></td>
													<td><input id="qtdEnvelopes" name="qtdEnvelopes" type="text" style="width:20px;"></td>
													<td align="right"><label>Box or Bag: </label></td>
													<td><input id="qtdBoxorBag" name="qtdBoxorBag" type="text" style="width:20px;"></td>
													<td align="right"><label>Other: </label></td>
													<td><input id="qtdOther" name="qtdOther" type="text" style="width:20px;"></td>
												</tr>
								</table>
								
								<table class="formLine" width="100%">
											<tr>
												<td><label>Comments</label></td>
												<td width="100%"><textarea id="unit" name="comments" rows="4" placeholder="Things like buzzer codes & specific instructions should go here." /></textarea></td>
											</tr>
											</table>
							</td>
						</tr>
					</table>
		</div>

			<br>
			
			<div class="orderButton" style="padding:10px;" align="center">
				<a id="orderSubmit" href="#"><span>Looks Good, Let's Go!</span></a>
				<!-- <input type="button" id="orderSubmit" class="big" value="Looks Good, Let's Go!"/> -->
				<div class="ajax_loading"><img src="<?php bloginfo( 'template_directory' ) ?>/images/ajax-loader.gif" />
				</div>
			</div>
				
			

    		</form>

            

		</div>

        
<? } 	else { 	
				echo '<p></p><h1>You need to login above or create an account below to place an order.</h1>';	
				
				echo do_shortcode('[wpcrl_register_form]');
				
			
			}	?>
		<?php 	

	}

}



geko_render_template();
